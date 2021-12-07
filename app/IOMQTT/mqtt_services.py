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


MQTTCON = MQTTConfiguration().instance

class MqttServices:
    def __init__(self,desc:str) -> None:
        self.desc = desc
        self.settingRequest : SettingRequest = SettingRequest(MQTTCON.REQUEST_RESEND_INTERVAL)

    def request_configuration(self,client_id:int,payload:str=None):
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
                payload=  {"client_id" : client_id , 'id' : None , "dt" : datetime.now()}
                payload = json.dumps(payload,indent=4,cls=DateTimeEncoder)

            mqtt_client.publish_topic(payload,client_id,ClientPublishTopic.RequestConfig.value)

            self.settingRequest.lastAttempt = datetime.now()
        except Exception as e :
            print(colored('MQTT send_configuration()','red'),f"{e.args}")
    
    def reply_event_changed(self,client_id:int,payload:str=None):
        try :
            # payload=  {"MqttServices" : 'send_configuration'}
            mqtt_client.publish_topic(payload,client_id,ClientPublishTopic.ReplyEvent)
        except Exception as e :
            print(colored('MQTT send_configuration()','red'),f"{e.args}")

    def reply_services(self,client_id:int,payload:str=None):
        try :
            # payload=  {"MqttServices" : 'send_configuration'}
            mqtt_client.publish_topic(payload,client_id,ClientPublishTopic.ReplyService)
        except Exception as e :
            print(colored('MQTT send_configuration()','red'),f"{e.args}")

    def resend_Message(self):
        # Resend Request Configuration
        try :
            if self.settingRequest.bolRequest is False :
                if self.settingRequest.attemptRequest():
                    MqttServices('rasp').request_configuration(MQTTCON.MAC_CLIENT_ID)
                    self.settingRequest.lastAttempt = datetime.now()
        except Exception as e :
            print(colored('MQTT send_configuration()','red'),f"{e.args}")

    def update_configration(self,payload:dict):
        ''' 
        #Returns None

        #Parameters:
            payload(dict) : The content to publish in python dict.
        
        #Return:
            None : Update MQTT configuration.
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
                
                mServices.resend_Message()
                
                if MQTTCON.BOL_IS_RECEIVED :
                    messsage_queue = _receive_incoming_message()

                    if len(messsage_queue) > 0 :
                        for message in messsage_queue :

                            # print(colored('MQTT receive_incoming_message()','blue'),message)

                            # split only the first occurence to obtain client id.
                            client_id = message['topic'].split('/',1)[0]

                            # split only the first occurence to eliminate client id , get the next element.
                            client_topic_without_forward_slash = message['topic'].split('/',1)[1]
                            client_payload = json.loads(message['msg'])
                            # decode_date = datetime.fromisoformat(client_payload['ts'])
                            # print(client_payload,"Received")

                            client_topic = "/" + client_topic_without_forward_slash

                            if client_topic == PublishTopic.Config.value :
                                # Receive setting from server , require to update Configuration
                                mServices.update_configration(client_payload)
                                pass
                            elif client_topic == PublishTopic.Ping.value :
                                # Receive ping from server , require reply pong
                                pass
                            elif client_topic == PublishTopic.ConfigUpdate.value :
                                # Receive config update from server , require to update Configuration
                                pass

                            # payload = json.dumps({"setting":{ "frequency" : 10}},indent=4, cls=DateTimeEncoder)
                            # mServices.send_configuration(client_id,payload)

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
