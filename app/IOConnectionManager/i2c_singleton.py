
from queue import Queue


class I2CConfiguration:
    class __OnlyOne:
        def __init__(self) -> None:
            self.BOL_IS_RECEIVED = True
            self.RECONNECT_INTERVAL = 15
            self.IS_CONNECTED = False

            # Queue to store i2c IO input 
            self.MESSAGE_QUEUE = Queue()

            # Mock IO
            self.BOL_MOCK_IO = True
      
    instance = None
    def __init__(self,arg=None) -> None:
        if not I2CConfiguration.instance :
            I2CConfiguration.instance = I2CConfiguration.__OnlyOne()
        else :
            I2CConfiguration.instance.val = arg
