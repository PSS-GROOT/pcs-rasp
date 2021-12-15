from threading import Thread
import time
from app.IOConnectionManager.i2c_singleton import I2CConfiguration
from app.IOMQTT.mqtt_singleton import MQTTConfiguration
from app.enum_type import LightEvent, TowerType, TowerTypeColor
from app.Utilities import helper_function as helperFunction

MQTTCON = MQTTConfiguration().instance
I2CCON = I2CConfiguration().instance
def mock_tower_io_drivers(tower_type : TowerType):
    loop_start = Thread(target=_mock, args=(tower_type,))
    loop_start.setName(f"I2C MOCK")
    loop_start.daemon = True
    loop_start.start()


def _mock(tower_type):
    mockUseCase = 'RUNNING' # 'ALERT' , 'WARNING'
    intFrequencyInterval : int = 1
    temp_data = [] # IO addresss from minimun 1 io address to 1,2,3,4,5 io address 
    currentCount = 0
    while True :
        intFrequency = MQTTCON.FREQUENCY

        # Reset counter , proceed to collection for next session
        if (currentCount > intFrequency) and (intFrequency != 0):
            # Add to queue only if not empty list
            if temp_data != [] :
                data = dict(data = temp_data ,address = ('port1','port2','port3') )
                I2CCON.MESSAGE_QUEUE.put(data)
                print("put data in queue", data)
                temp_data = []

            # Reset counter 
            currentCount = 0
            temp_data = []
            print("Reset counter and empty data")
        elif intFrequency == 0 :
            currentCount = 0
            temp_data = []
            print("Reset counter and empty data due to configuration frequency is still 0.")
        else :
            # mock data for each frequency interval
            output = helperFunction.getTowerColorGroup(tower_type=tower_type)
            # print(output)
        

            data_list =[2] * len(output)
            # e.g data_list = [2,2,2]

            if mockUseCase == "RUNNING":             
                if tower_type.value >= 3 :
                    data_list[2] = 1
                    # temp_data.append((LightEvent.SolidOff.value,LightEvent.SolidOff.value,LightEvent.SolidOn.value))              
            elif mockUseCase == "WARNING":
                if tower_type.value >= 2:
                    data_list[1] = 1
            elif mockUseCase == "ALERT":
                data_list[0] = 1
            else :
                # mock random usecase
                pass

            data_list = tuple(data_list)
            temp_data.append(data_list)
            # print("append data",data_list)


        currentCount += 1
        
        # print(currentCount,'currentCount')
        time.sleep(intFrequencyInterval)