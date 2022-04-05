
from datetime import datetime
from queue import Queue

from app.enum_type import TowerType


class MQTTConfiguration:
    class __OnlyOne:
        def __init__(self) -> None:

            # Mqtt Setting (Update from server)
            self.CLIENT_ID = None
            self.RECONNECT_INTERVAL = 15
            self.TOWER_TYPE = TowerType.Three
            self.FREQUENCY = 0.1
            self.SESSION_LIMIT_COUNT = 20
            self.INTERVAL_UPDATE = 30
            self.BOL_INTERVAL_UPDATE = True
            
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
        
        def addErrorMessage(self,errorDesc):
            self.SEND_MESSAGE_QUEUE.put([errorDesc,'/client/error',None])

      
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