import json
from threading import Thread
from typing import List, Mapping
from termcolor import colored
import time
from datetime import datetime
from json import JSONEncoder


# module
from app.IOMQTT.mqtt_singleton import MQTTConfiguration, SettingRequest 
from app.enum_type import ClientPublishTopic, PublishTopic
from app.Utilities.helper_function import DateTimeEncoder
from app.IOMQTT import mqtt_client
from app.IOMQTT.mqtt_interface import MqttClientInterface


MQTTCON = MQTTConfiguration().instance

class MqttServices(MqttClientInterface):
    def __init__(self,desc:str) -> None:
        self.desc = desc
        self.settingRequest : SettingRequest = SettingRequest(MQTTCON.REQUEST_RESEND_INTERVAL)

    def request_configuration(self,mac_client_id:int,payload:str=None):
        ''' 
        #Returns None

        #Parameters:
            client_id(int) : The targeted remote client id 
            payload(str) : The content to publish , must dumps and serialize into into json str
        
        #Return:
            None : Broadcast and emit message to broker
        '''

        try :
            if payload is None :
                payload=  {"mac_client_id" : mac_client_id , 'client_id' : None , "dt" : datetime.now()}
                payload = json.dumps(payload,indent=4,cls=DateTimeEncoder)

            mqtt_client.publish_topic(payload,mac_client_id,ClientPublishTopic.RequestConfig.value)

            self.settingRequest.lastAttempt = datetime.now()
        except Exception as e :
            print(colored('MQTT request_configuration()','red'),f"{e.args}")
    
    def reply_event_changed(self,event_status:str=None):
        ''' 
        #Returns None

        #Parameters:
            event_status(list) : The light event for each address. 
                                 e.g = [1,1,0] The element order is follow according to the address of raspberryPI IO.
        
        #Return:
            None : Broadcast and emit message to broker
        '''

        try :
            payload = dict(
                light_event = event_status ,
                mac_client_id = MQTTCON.MAC_CLIENT_ID ,
                client_id = MQTTCON.CLIENT_ID ,
                tower_type = MQTTCON.TOWER_TYPE
            )
            payload = json.dumps(payload,indent=4,cls=DateTimeEncoder)
            mqtt_client.publish_topic(payload,MQTTCON.MAC_CLIENT_ID,ClientPublishTopic.ReplyEvent.value)
        except Exception as e :
            print(colored('MQTT reply_event_changed()','red'),f"{e.args}")

    def reply_services(self,server_status:str):
        ''' 
        #Returns None

        #Parameters:
            event_status(<ServiceStatus(Enum).value : str) : The raspberry pi to i2c IO connection status in string.
        
        #Return:
            None : Broadcast and emit message to broker
        '''
        try :
         
            payload = dict(
                status = server_status ,
                mac_client_id = MQTTCON.MAC_CLIENT_ID ,
                client_id = MQTTCON.CLIENT_ID ,
            )
            payload = json.dumps(payload,indent=4,cls=DateTimeEncoder)      
            mqtt_client.publish_topic(payload,MQTTCON.MAC_CLIENT_ID,ClientPublishTopic.ReplyService.value)
        except Exception as e :
            print(colored('MQTT reply_services()','red'),f"{e.args}")

    def reply_error(self,message:str=None):
        try :
            mac_client_id = MQTTCON.MAC_CLIENT_ID

            payload = dict(
                message = message ,
                mac_client_id = mac_client_id ,
                client_id = MQTTCON.CLIENT_ID ,
            )
            payload = json.dumps(payload,indent=4,cls=DateTimeEncoder)
            mqtt_client.publish_topic(payload,mac_client_id,ClientPublishTopic.ReplyErrorLog.value)
        except Exception as e :
            print(colored('MQTT reply_error()','red'),f"{e.args}")
    
    def reply_ack(self,ack_type=str):
        try :
            mac_client_id = MQTTCON.MAC_CLIENT_ID

            payload = dict(
                mac_client_id = mac_client_id ,
                client_id = MQTTCON.CLIENT_ID ,
                ack_type = ack_type
            )

            payload = json.dumps(payload,indent=4,cls=DateTimeEncoder)
            mqtt_client.publish_topic(payload,mac_client_id,ClientPublishTopic.ReplyAck.value)
        except Exception as e :
            print(colored('MQTT reply_ack()','red'),f"{e.args}")
    
    def reply_pong(self):
        try :
            mac_client_id = MQTTCON.MAC_CLIENT_ID

            payload = dict(
                mac_client_id = mac_client_id ,
                client_id = MQTTCON.CLIENT_ID ,
            )
            payload = json.dumps(payload,indent=4,cls=DateTimeEncoder)
            mqtt_client.publish_topic(payload,mac_client_id,ClientPublishTopic.ReplyPong.value)
        except Exception as e :
            print(colored('MQTT reply_pong()','red'),f"{e.args}")


    def resend_message(self):
        # Resend Request Configuration
        try :
            if self.settingRequest.bolRequest is False :
                if self.settingRequest.attemptRequest():
                    self.request_configuration(MQTTCON.MAC_CLIENT_ID)
                    self.settingRequest.lastAttempt = datetime.now()
        except Exception as e :
            print(colored('MQTT send_configuration()','red'),f"{e.args}")

    def update_configuration(self,payload:dict):
        ''' 
        #Returns None

        #Parameters:
            payload(dict) : The key pair value to update MQTT configuration.
        
        #Return:
            None 
        '''

        try :
            for key,value in payload.items() :     
                capitalKey = key.upper()  
                setattr(MQTTCON, capitalKey,value)
                print(colored('MQTT Update Config','blue'),f"Update attribute {capitalKey} value to {value}")

            self.settingRequest.bolRequest = True
            print(colored('MQTT Request','blue'),f"Configuration acquired, rasp will stop request setting.")
        except Exception as e :
            print(colored('MQTT update_configration()','red'),f"{e.args}")
    

def _receive_incoming_message()-> list:
    ''' 
        #Returns execution_queue 

        #Parameters:
            None
        
        #Return:
            execution_queue : List of message 
            element inside the list is type of : e.g {'topic': '0x106530ea239e/client/setting', 'msg': '{"id": "1234", "ts": "11/26/2021, 16:14:17.993417"}
           
    '''
    try :
        execution_queue = []
        # pop incoming queue , add to another execution_queue variable
        while len(mqtt_client.mqtt_incoming_msg.queue) > 0:

            message = mqtt_client.mqtt_incoming_msg.get()

            execution_queue.append(message)

            mqtt_client.mqtt_incoming_msg.task_done()

        return execution_queue

    except Exception as e :
        print(colored('MQTT receive_incoming_message()','red'),f"{e.args}")



def mqtt_consumer():
    def _loop_start():
        while True :
            try :
                
                mServices.resend_message()
                
                if MQTTCON.BOL_IS_RECEIVED :
                    messsage_queue = _receive_incoming_message()

                    if len(messsage_queue) > 0 :
                        for message in messsage_queue :
                      
                            # split only the first occurence to obtain client id.
                            client_id = message['topic'].split('/',1)[0]

                            # split only the first occurence to eliminate client id , get the next element.
                            client_topic_without_forward_slash = message['topic'].split('/',1)[1]
                            client_payload = json.loads(message['msg'])                  
                            client_topic = "/" + client_topic_without_forward_slash

                            if client_topic == PublishTopic.Config.value :
                                # Receive setting from server , require to update Configuration
                                mServices.update_configuration(client_payload)
                                pass
                            elif client_topic == PublishTopic.Ping.value :
                                # Receive ping from server , require reply pong
                                mServices.reply_pong()
                                pass
                            elif client_topic == PublishTopic.ConfigUpdate.value :
                                # Receive config update from server , require to update Configuration
                                mServices.update_configuration(client_payload)
                                mServices.reply_ack(client_topic)
                                pass
                                                   
                    # TURN OFF THE FLAG
                    MQTTCON.BOL_IS_RECEIVED = False
                
                time.sleep(0.5)
            except Exception as e :
                print(colored('MQTT mqtt_consumer()','red'),f"{e.args}")
    
    # Consumer driver code
    mServices = MqttServices('rasp')
    mServices.request_configuration(MQTTCON.MAC_CLIENT_ID)

    loop_start = Thread(target=_loop_start, args=())
    loop_start.setName(f"MQTT Client")
    loop_start.daemon = True
    loop_start.start()
