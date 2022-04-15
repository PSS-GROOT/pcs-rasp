
from datetime import datetime
from queue import Queue
from app import load_config

from app.enum_type import ClientPublishTopic, TowerType


class MQTTConfiguration:
    class __OnlyOne:
        def __init__(self) -> None:

            # Mqtt Setting (Update from server)
            self.CLIENT_ID = None
            self.RECONNECT_INTERVAL = 15
            self.TOWER_TYPE = None
            self.FREQUENCY = 0.1
            self.LIMIT_FREQUENCY = 20
            self.MULTIPLIER = self.LIMIT_FREQUENCY / 20
            self.INTERVAL_UPDATE = 30
            self.BOL_INTERVAL_UPDATE = True 
            self.DEBUG = load_config.DEBUG
            
            # Mqtt Resend Setting
            self.EVENT_RESEND_INTERVAL = 10
            self.BOL_RESEND = True

            # Mqtt Constant
            self.BOL_IS_RECEIVED = True
            self.MAC_CLIENT_ID = None
     
            # Request Setting Constant
            self.BOL_SETTING_SUCCESS = False
            self.REQUEST_RESEND_INTERVAL = 10

            # Outgoing Queue
            self.SEND_MESSAGE_QUEUE = Queue()
            self.RESEND_QUEUE = Queue()

            # I2C Pattern setting
            self.FAST_FLASH = [0.08, 0.12]       # Interval flash between On and Off atleast 0.08 seconds to 0.12 seconds
            self.SLOW_FLASH = [0.4, 0.8]         # Interval flash between On and Off atleast 0.8 seconds to 1.2 seconds
            self.SOLID_ON = [0.9, 2.1]           # Continous On atleast 8 times * 1  e.g 11111111 to 12 times * 1
            self.SOLID_OFF = [0.9, 2.1]          # Continous Off Atleast 8 * 2 e.g 2222 2222  to 12 * 1
            self.FLASH_ON_ONCE = [0.3, 0.6]
            self.FLASH_OFF_ONCE = [0.3, 0.6]
        
        def addErrorMessage(self,errorDesc):
            self.SEND_MESSAGE_QUEUE.put([errorDesc,ClientPublishTopic.ReplyErrorLog.value,None])

        def rangeData(self)-> str:
            data = {
                'FAST_FLASH' : self.FAST_FLASH ,
                'SLOW_FLASH' :  self.SLOW_FLASH  ,
                'SOLID_ON' :   self.SOLID_ON ,
                'SOLID_OFF' : self.SOLID_OFF   ,
                'FLASH_ON_ONCE' : self.FLASH_ON_ONCE ,
                'FLASH_OFF_ONCE' : self.FLASH_OFF_ONCE 
            }
            return data


      
    instance = None
    def __init__(self,arg=None) -> None:
        if not MQTTConfiguration.instance :
            MQTTConfiguration.instance = MQTTConfiguration.__OnlyOne()
        else :
            MQTTConfiguration.instance.val = arg


class SettingRequest():
    def __init__(self,requestInterval:int ) -> None:
        self.requestInterval = requestInterval  # interval for retry
        self.bolRequest = False                 # if True stop resend
        self.lastAttempt = datetime.now()       # last attempt datetime

    def attemptRequest(self)-> bool :
        elapse = datetime.now() - self.lastAttempt
        if elapse.seconds >= self.requestInterval :
            return True
        else :
            return False