
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
            self.BOL_MOCK_IO = False

            # I2C STATE
            self.STATE = None               # NOT IN USE
            self.ADDRESS_MAPPING = None     # NOT IN USE

            # I2C REAL TIME SIGNAL
            self.REAL_TIME_SIGNAL = None # [2,2,2,2,2]

    instance = None
    def __init__(self,arg=None) -> None:
        if not I2CConfiguration.instance :
            I2CConfiguration.instance = I2CConfiguration.__OnlyOne()
        else :
            I2CConfiguration.instance.val = arg
