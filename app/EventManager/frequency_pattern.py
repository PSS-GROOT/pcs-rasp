
from typing import List, Tuple
from app.IOMQTT.mqtt_singleton import MQTTConfiguration


MQTTCON = MQTTConfiguration().instance

# Rules & Pattern (Sort by priority)
# Consecutive on (n alphabet for each color on)
# Consecutive off (n alphabet for each color off)



class FrequencyManager():
    def __init__(self) -> None:
        self.PatternVariants : List[PatternVariant] = []
        self.IncomingData : List[tuple] = None

        # Decide Pattern
        self.PatternFactory()

        # # Execute Pattern
        # self.PatternProcessor()

    def addIncomingData(self,incomingData : List[Tuple]):
        self.IncomingData = incomingData


    def PatternFactory(self):
        self.PatternVariants.append(PV.PatternSolidOn)
        self.PatternVariants.append(PV.PatternSolidOff)
        self.PatternVariants.append(PV.PatternSlowFlash)
        self.PatternVariants.append(PV.PatternFastFlash)
        # print(self.PatternVariants)

    def PatternProcessor(self,address:tuple):
        
        resultList = dict()
        for _data , _address in zip(self.IncomingData,address):
      
            print(f"Accessing : {_data},{_address}")
            resultList[_address] = None

            for func in self.PatternVariants :
                if func(_data) : 
                    resultList[_address] = func.__name__
                    print(f"Rules MATCHED - {func.__name__}")
                    break
                else :
                    print(f"Rules FAILED - {func.__name__} next rules")

            # if no rules match
            if resultList[_address] == None :
                resultList[_address] = 'UNKNOWN'
                print(resultList,"Set UNKNOWN")
            

        return resultList   


class PatternVariant():
    def __init__(self):
        pass
        '''
        # Solid On - each signal in same batch solid on. (1),(1),(1),(1),(1),(1)
        # Solid Off - each signal in same batch solid off. (1),(1),(1),(1),(1),(1)
        # FastFlash - each signal in same batch flashing. (1),(2),(1),(2),(1),(2)
        # SlowFlash - each signal in current batch and next batch flashing. (1),(1),(2),(2),(1),(1),(2),(2)

        # The pattern variant's algorithms should dynamic change according to MQTTCON.FREQUENCY.

        # How if frequency update from 10 to 15 ?
        # How if frequency update from 10 to 2 ?
            # FastFlash and SlowFlash valid condition for minimun criteria require atleast
                # a. FastFlash - minimun FREQUENCY = 2
                # B. SlowFlash - minimum FREQUENCY = 4

        '''

    def PatternSolidOn(self,data):
        targetSignal = 1
        for j in data :
            if j != targetSignal :
                return False

        return True

    def PatternSolidOff(self,data):
        targetSignal = 2
        for j in data :
            if j != targetSignal :
                return False

        return True

    def PatternFastFlash(self,data):
        # first signal either on or off also can
        # 1212121212
        # 2121212121
        firstSignal = data[0]
        nextSignal = data[1]

        # Eliminate this rules approved solid on and solid off by introduce 1st and 2nd rules must not be same
        if firstSignal != nextSignal :

            # Get the first signal and 3rd and following signal for validate
            for i in range(0,len(data),2):
                # print(f"{i} is data {data[i]}")
                if data[i] != firstSignal :
                    return False

            # Get 2nd signal and 4th signal and following signal for validate
            for i in range(1,len(data),2):
                # print(f"{i} is data {data[i]}")
                if data[i] != nextSignal :
                    return False

            return True
        else :
            return False
    
    def PatternSlowFlash(self,data):
        pass

PV = PatternVariant()