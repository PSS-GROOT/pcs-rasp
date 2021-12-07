
import time
import datetime
from termcolor import colored
from app.IOConnectionManager.i2c_singleton import I2CConfiguration

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
    while True :

        message = _i2cMessageIncoming()
        
        for _message in message :
            pass
            #TODO transfrom and normalize i2c data to event , broadcast to server

        time.sleep(30)
        print(f"{datetime.datetime.now()} Thread i2cHandler")