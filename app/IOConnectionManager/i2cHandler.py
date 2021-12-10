
import time
import datetime
from termcolor import colored
from app.IOConnectionManager.i2c_singleton import I2CConfiguration
from app.IOConnectionManager import mock_i2c as MockI2C
from app.enum_type import TowerType

I2CCONT = I2CConfiguration().instance

def _i2cMessageIncoming():
    try :
        execution_queue = []
        # pop incoming queue , add to another execution_queue variable
        while len(I2CCONT.MESSAGE_QUEUE.queue) > 0:

            message = I2CCONT.MESSAGE_QUEUE.get()

            execution_queue.append(message)

            I2CCONT.MESSAGE_QUEUE.task_done()

        return execution_queue

    except Exception as e :
        print(colored('MQTT receive_incoming_message()','red'),f"{e.args}")


def i2cConnection():
    pass

def i2cHandler():
    if I2CCONT.BOL_MOCK_IO is True :
        # Create mock IO thread
        MockI2C.mock_tower_io_drivers(tower_type=TowerType.Three)
    else :
        # Real i2c connection and input
        pass

    while True :

        message = _i2cMessageIncoming()
        
        for _message in message :
            print(colored('i2c Incoming','cyan'),f"{_message} , len={len(_message)}")
            # e.g _message = [(2, 2, 1), (2, 2, 1), (2, 2, 1), (2, 2, 1), (2, 2, 1), (2, 2, 1), (2, 2, 1), (2, 2, 1), (2, 2, 1), (2, 2, 1)] , len=10 
            
            # Now unzip list of tuple , group by color  
            # e.g unzipped_list = [(2, 2, 2, 2, 2, 2, 2, 2, 2, 2), (2, 2, 2, 2, 2, 2, 2, 2, 2, 2), (1, 1, 1, 1, 1, 1, 1, 1, 1, 1)]
            unzipped_object = zip(*_message)
            unzipped_list = list(unzipped_object)  
            print(unzipped_list)
            
            #TODO transfrom and normalize i2c data to event , broadcast to server

        time.sleep(2)
        # print(f"{datetime.datetime.now()} Thread i2cHandler")