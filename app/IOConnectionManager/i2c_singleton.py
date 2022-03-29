
from queue import Queue


class I2CConfiguration:
    class __OnlyOne:
        def __init__(self) -> None:
            self.BOL_IS_RECEIVED = True
            self.RECONNECT_INTERVAL = 15
            self.IS_CONNECTED = False

            # I2C Queue to store i2c IO input 
            self.MESSAGE_QUEUE = Queue()

            # I2C Mock IO
            self.BOL_MOCK_IO = True

            # I2C STATE
            self.STATE = None
            self.ADDRESS_MAPPING = None
      
    instance = None
    def __init__(self,arg=None) -> None:
        if not I2CConfiguration.instance :
            I2CConfiguration.instance = I2CConfiguration.__OnlyOne()
        else :
            I2CConfiguration.instance.val = arg
