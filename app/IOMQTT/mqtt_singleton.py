
from datetime import datetime


class MQTTConfiguration:
    class __OnlyOne:
        def __init__(self) -> None:

            # Mqtt Setting (Update from server)
            self.CLIENT_ID = None
            self.RECONNECT_INTERVAL = 15
            self.TOWER_TYPE = None
            self.FREQUENCY = 0

            # Mqtt Constant
            self.BOL_IS_RECEIVED = True
            self.MAC_CLIENT_ID = None
     
            # Request Setting Constant
            self.BOL_SETTING_SUCCESS = False
            self.REQUEST_RESEND_INTERVAL = 3

      
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