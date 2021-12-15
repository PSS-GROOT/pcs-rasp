

import time,sys,os

# sys.path.append(os.getcwd())
import datetime
from termcolor import colored
from app.IOConnectionManager.i2c_singleton import I2CConfiguration
from app.IOConnectionManager import mock_i2c as MockI2C
from app.IOMQTT.mqtt_singleton import MQTTConfiguration
from app.enum_type import TowerType
from app.EventManager import frequency_pattern as FrequencyPattern

MQTTCON = MQTTConfiguration().instance
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
        print(colored('MQTT receive_incoming_message()','red'),e.args)

def i2cConnection():
    pass

def i2cHandler():
    if I2CCONT.BOL_MOCK_IO is True :
        # Create mock IO thread
        MockI2C.mock_tower_io_drivers(tower_type=TowerType.Three)
    else :
        # Real i2c connection and input
        pass

    FP = FrequencyPattern.FrequencyManager()

    while True :

        message = _i2cMessageIncoming()
        
        for _message in message :
            print(colored('i2c Incoming','cyan'),f"{_message} , len={len(_message)}")

            if len(_message['data']) == MQTTCON.FREQUENCY :

                # e.g _message = {
                #                   "data" : [(2, 2, 1), (2, 2, 1), (2, 2, 1), (2, 2, 1), (2, 2, 1), (2, 2, 1), (2, 2, 1), (2, 2, 1), (2, 2, 1), (2, 2, 1)] ,
                #                   "address" : (port1,port2,port3)
                #                }


                # e.g unzipped_list = [(2, 2, 2, 2, 2, 2, 2, 2, 2, 2), (2, 2, 2, 2, 2, 2, 2, 2, 2, 2), (1, 1, 1, 1, 1, 1, 1, 1, 1, 1)]                
                unzipped_object = zip(*_message['data'])
                unzipped_list = list(unzipped_object)  
                print(unzipped_list)
                
                # Transfrom and Normalize i2c data to event , broadcast to server
                FP.addIncomingData(unzipped_list)
                result = FP.PatternProcessor(_message['address'])

                #e.g result = 'port1': 'UNKNOWN', 'port2': 'PatternSolidOff', 'port3': 'PatternSolidOn'}

                # TODO detect changes on broadcast

            else :
                print(colored('I2C Incoming Message','red'),f"Invalid message length compared to MQTTCON.FREQUENCY {MQTTCON.FREQUENCY}")
                

        time.sleep(2)
        # print(f"{datetime.datetime.now()} Thread i2cHandler")


if __name__ == '__main__' :
    # print("i2chandler invoke")
    # python -m app.IOConnectionManager.i2cHandler
    pass
