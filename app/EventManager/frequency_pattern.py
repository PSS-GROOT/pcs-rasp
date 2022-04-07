
''' 

This module define the pattern to capture , and frequency manager that plug all those 
pattern variants and return a set of results 

'''

from typing import List, Tuple

from termcolor import colored
from app.IOMQTT.mqtt_singleton import MQTTConfiguration
from app.Utilities import helper_function
from app.enum_type import LightEvent


MQTTCON = MQTTConfiguration().instance


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
        self.PatternVariants.append(PV.SolidOn)
        self.PatternVariants.append(PV.SolidOff)
        self.PatternVariants.append(PV.SlowFlashing)
        self.PatternVariants.append(PV.FastFlashing)
        self.PatternVariants.append(PV.FlashOffOnce)
        self.PatternVariants.append(PV.FlashOnOnce)
        # print(self.PatternVariants)

    def PatternProcessor(self,address:tuple):
        
        resultList = dict()
        for _data , _address in zip(self.IncomingData,address):
      
            print(f"Accessing : {_data},{_address}")
            resultList[_address] = None

            for func in self.PatternVariants :
                if func(_data) : 
                    lightEnum = LightEvent[func.__name__]
                    resultList[_address] =  dict(type=lightEnum._name_,code=lightEnum.value)
                    print(colored(f"Rules MATCHED - {func.__name__}",'green'))
                    break
                else :
                    print(colored(f"Rules FAILED - {func.__name__}",'red'))

            # if no rules match
            if resultList[_address] == None :
                resultList[_address] =  dict(type=LightEvent.Unknown._name_,code=LightEvent.Unknown.value)
                print(colored(f"Rules Unknown MATCHED - {LightEvent.Unknown._name_}",'green'))
               

        return resultList   


class PatternVariant():
    def __init__(self):
        pass
        '''
        # Solid On - each signal in same batch solid on. (1),(1),(1),(1),(1),(1)
        # Solid Off - each signal in same batch solid off. (2),(2),(2),(2),(2),(2)
        # FastFlash - each signal in same batch flashing. (1),(2),(1),(2),(1),(2)
        # SlowFlash - each signal in current batch and next batch flashing. (1),(1),(2),(2),(1),(1),(2),(2)

        # The pattern variant's algorithms should dynamic change according to MQTTCON.FREQUENCY.

        # How if frequency update from 10 to 15 ?
        # How if frequency update from 10 to 2 ?
            # FastFlash and SlowFlash valid condition for minimun criteria require atleast
                # a. FastFlash - minimun FREQUENCY = 2
                # B. SlowFlash - minimum FREQUENCY = 4

        '''
    @helper_function.log_error()
    def SolidOn(self,data):
        targetSignal = 1
        for j in data :
            if j != targetSignal :
                return False

        return True

    @helper_function.log_error()
    def SolidOff(self,data):
        targetSignal = 2
        for j in data :
            if j != targetSignal :
                return False

        return True

    @helper_function.log_error()
    def FastFlashing(self,data):
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
    
    @helper_function.log_error()
    def SlowFlashing(self,data):
        if MQTTCON.SESSION_LIMIT_COUNT == 20 :
            # Pattern 1 = 11111111112222222222
            # Pattern 2 = 22222222221111111111
            halfLength = int(len(data)/2)
            firstHalf = secondHalf2nd = data[:halfLength]
            secondHalf = firstHalf2nd = data[halfLength:]

            # Check if both chunk different value
            # Validate pattern 1
            if firstHalf != secondHalf :
                getFirstValue = firstHalf[0]
                getFirstValueSecondHalf = secondHalf[0]
                firstResult = all(x == getFirstValue for x in firstHalf)
                secondResult = all(x == getFirstValueSecondHalf for x in secondHalf)

                if firstResult and secondResult :
                    return True

            # Validate pattern 2
            if firstHalf2nd != secondHalf2nd :
                getFirstValue = firstHalf2nd[0]
                getFirstValueSecondHalf = secondHalf2nd[0]
                firstResult = all(x == getFirstValue for x in firstHalf2nd)
                secondResult = all(x == getFirstValueSecondHalf for x in secondHalf2nd)

                if firstResult and secondHalf :
                    return True

            return False

    @helper_function.log_error()
    def FlashOffOnce(self,data):
        #Pattern 1 = 111111111211111111
        # The off can happen in any index
        off = 2
        
        if data.count(off) == 1 :
            return True

        return False

    @helper_function.log_error()
    def FlashOnOnce(self,data):
        #Pattern 1 = 22222221222222
        # The on can happen in any index
        on = 1
        
        if data.count(on) == 1 :
            return True

        return False

PV = PatternVariant()