from collections import deque
from threading import Thread
import paho.mqtt.client as mqtt
from queue import Queue
from termcolor import colored, cprint
import time
import datetime
from json import JSONEncoder

# module
from app import load_config
from app.IOMQTT.mqtt_singleton import MQTTConfiguration
from app.enum_type import ClientPublishTopic, PublishTopic


mqtt_incoming_msg = Queue()
mqtt_outgoing_msg = Queue()

client : mqtt.Client = None
connected = False
MQTTCON = MQTTConfiguration().instance



status_code = {
0   :"Connection accepted" ,
1   :"Connection refused, unacceptable protocol version",
2	:"Connection refused, identifier rejected",
3	:"Connection refused, server unavailable",
4	:"Connection refused, bad user name or password",
5	:"Connection refused, not authorized",
}



def init_client(type:str, name:str, client_id=None):
    MQTTCON.MAC_CLIENT_ID = client_id

    loop_start = Thread(target=connect_client, args=(client_id,type))
    loop_start.setName(name)
    loop_start.daemon = True
    loop_start.start()




def connect_client(client_id = None,instance_type='server'):
    """ Create mqtt client constructor , connect to mqtt broker, invoke selection either server or rasp """  
    try :
            def subscribeTopic():     
                if instance_type == 'server' :
                    subscribe_topic()
                else :     
                    if client_id is None :         
                        from uuid import getnode as get_mac
                        mac = get_mac()
                        mac = hex(get_mac())
                        client_subscribe_topic(client_id=mac)
                    else :
                        client_subscribe_topic(client_id=client_id)
           
            def registerCallback():
                # register method to mqtt callback event
                client.on_connect = on_connect
                client.on_message = on_message
                client.on_disconnect = on_disconnect
            
            def connectBroker()-> int:
                try :
                    # The default keep alive period for the Python MQTT client is 60 secs, but it can be set to anything you want when you establish the client connection.
                    result = client.connect(host=load_config.MQTT_HOST,port=1883, keepalive=300)
                    print(colored('MQTT','green'),f"Mosquitto Broker connected. {status_code.get(result)}")
                    return True

                except Exception as e :
                    print(colored('MQTT','red'),f"Mosquitto on host server is not running, please verify the host machine IP {load_config.MQTT_HOST}:1883, Exception:{e.args}")
                    return None
               

            global client , connected
            connected = False
            while True :

                if connected == False :  
                    print('Instantiated mqtt.Client()',client_id)
                    client = mqtt.Client(client_id)
                    # print(client)
                    result = connectBroker()
                    # print(result)
                    if result :
                        connected = True
                        # The loop_start() starts a new thread, that calls the loop method at regular intervals for you. It also handles re-connects automatically.
                        # To stop the loop use the loop_stop() method. 
                        subscribeTopic()  
                        registerCallback()   
                        client.loop_start()
                        # print(client)
                        msg = "MQTT Client loop_start()"
                        print(colored('MQTT','green'),msg)
                    else :
                        print(colored('MQTT','red'),"Require reconnect to mqtt broker, please ensure Mosquitto broker is running at host machine.")
                        time.sleep(MQTTCON.RECONNECT_INTERVAL)
                else :
                    ## mock another client to connect to mqtt
                    check_wifi_client = mqtt.Client(f"CHECK_WIFI_CLIENT{client_id}")
                    result = connectBroker()
                    if result == None :
                        print(colored('MQTT','red'),f"Detected connection loss")
                        connected = False
                        client.disconnect()
                    else :
                        check_wifi_client.disconnect()
                        

                    time.sleep(1)
                                     
    except Exception as e :
        print(colored('MQTT','red'),e.args)
        return None


#region Event 
def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    #print("Connected with result code " + str(rc))
    # display message
    msg = f"Mqtt Client starting up on {client._host}, connected code {rc}\n"
    print(colored('MQTT','green'),msg)



def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server/broker which might forwarded by other clients."""
    msg.payload = msg.payload.decode("utf-8")

    mqtt_incoming_msg.put({"topic": msg.topic ,"msg": msg.payload})
    print(colored('MQTT Incoming','green'),f" on_message Received from {msg.topic} - {msg.payload}")

    MQTTCON.BOL_IS_RECEIVED = True

def on_disconnect(client, userdata, rc=0):
    """The callback for when disconnected from the broker."""
    global connected
    client.loop_stop()
    msg = "Mqtt Client Disconnected."
    print(colored('MQTT','green'),msg)
    connected = False

#endregion

def mqtt_broadcast(msg, topic,qos=0,retain=False):
    """ encapsulate send message hence other module does not require to import the client object and not accessible to client object, they can use this function send message to specific topic """
    try :
        if client :
            client.publish(topic, msg, qos=qos, retain=retain)
            if ClientPublishTopic.ReplySignalRealTime.value not in topic :
                print(colored('MQTT Outgoing','green'),f"{msg},\n to {topic}")
        else :
            print(colored('MQTT','green'),f"mqtt_broadcast() unable to broadcast due to client is None {client}.")
    except Exception as e :
        print(colored('MQTT','red'),f"mqtt_broadcast() {e.args}")

def subscribe_topic():
    # Embed a unique identifier or the Client Id into the topic
    # single level wildcard "+" subscribe any topic matches a topic with single-level wildcard if it contains an arbitrary string 
    try :
        for e in ClientPublishTopic :
            topic =  f"+{e.value}"

            client.subscribe(topic)
            print(colored('MQTT subscribe_topic()','green'),topic)
    except Exception as e :
        print(colored('MQTT subscribe_topic()','red'),e.args)

def client_subscribe_topic(client_id:str):
    for e in PublishTopic :
        topic = f"{client_id}{e.value}"

        if e.value == '/server/event':
            client.subscribe(topic,qos=2)
            print(colored('MQTT subscribe_topic()','green'),f"{topic} , qos {2}")
        else :
            client.subscribe(topic)
        print(colored('MQTT subscribe_topic()','green'),topic)

def publish_topic(payload,client_id:int, topic_selection:str,qos:int=0,retain=False):
    topic =  f"{client_id}{topic_selection}"
    mqtt_broadcast(payload,topic,qos,retain)

