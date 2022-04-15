
from itertools import cycle
from typing import List
from app import load_config
from app.IOMQTT.mqtt_singleton import MQTTConfiguration
from app.Utilities import helper_function
from termcolor import colored

from app.enum_type import LightEvent

MQTTCON = MQTTConfiguration().instance

class PatternVariantInterval():
    def __init__(self):
        self.PatternToCapture = None
    
    @staticmethod
    def calDuration(a):
        return round(a * MQTTCON.FREQUENCY,2)

    def printConsole(self,data,fromTime,toTime,accumulateList,bolResult):
        if load_config.DEBUG is True :
            debugLog = dict(data = data ,
                fromTime = fromTime ,
                toTime =toTime,
                accumulateList =accumulateList ,
                accumulateDuration = list(map(self.calDuration,accumulateList)) ,
                result = bolResult
                )
            
            color = "green" if bolResult else "red"
            print(colored(f"{bolResult}",color),debugLog )


    @helper_function.log_error()
    def SolidOn(self,data):
        fromTime = MQTTCON.SOLID_ON[0] * MQTTCON.MULTIPLIER
        toTime = MQTTCON.SOLID_ON[1] * MQTTCON.MULTIPLIER
        accumulateList = []
        accumulateCounter = 0
        bolResult = False

        if data and len(data) > 0 :        
            targetSignal = 1
            for count,j in enumerate(data) :
                if j == targetSignal :
                    accumulateCounter +=1
                else :
                    # Accumulater break , add to counter for 1st chunks
                    accumulateList.append(accumulateCounter)
                    accumulateCounter = 0
                
                if count == len(data) - 1 :
                    # Add counter to list for last element
                    # skip 0 , above logic condition had added counter value 0
                    if accumulateCounter != 0 :
                        accumulateList.append(accumulateCounter)

            # Check
            for x in accumulateList :
                totalTime = self.calDuration(x)
                if totalTime >= fromTime and totalTime <= toTime :
                    bolResult = True
                    
      
        self.printConsole(data,fromTime,toTime,accumulateList,bolResult)

        return bolResult

    @helper_function.log_error()
    def SolidOff(self,data):
        fromTime = MQTTCON.SOLID_OFF[0] * MQTTCON.MULTIPLIER
        toTime = MQTTCON.SOLID_OFF[1] * MQTTCON.MULTIPLIER
        accumulateList = []
        accumulateCounter = 0
        bolResult = False

        if data and len(data) > 0 :        
            targetSignal = 2
            for count,j in enumerate(data) :
                if j == targetSignal :
                    accumulateCounter +=1
                else :
                    # Accumulater break , add to counter for 1st chunks
                    accumulateList.append(accumulateCounter)
                    accumulateCounter = 0
                
                if count == len(data) - 1 :
                    # Add counter to list for last element
                    # skip 0 , above logic condition had added counter value 0
                    if accumulateCounter != 0 :
                        accumulateList.append(accumulateCounter)

            # Check
            for x in accumulateList :
                totalTime = self.calDuration(x)
                if totalTime >= fromTime and totalTime <= toTime :
                    bolResult = True
                    
      
        self.printConsole(data,fromTime,toTime,accumulateList,bolResult)

        return bolResult
       

    @helper_function.log_error()
    def FastFlashing(self,data):
        # Capture the interval when light event occur
        # a. switch from on to off 
        # b. switch from off to on

        if not data : 
            return False
    
        fromTime = MQTTCON.FAST_FLASH[0] * MQTTCON.MULTIPLIER
        toTime = MQTTCON.FAST_FLASH[1] * MQTTCON.MULTIPLIER
        accumulateList = []
        accumulateCounter = 1
        bolResult = False

        # print(data,"data")
        curr = None
        for x in data :
            if curr == None :
                curr = x
            else :
                if x != curr :
                    # Detect changes , add accumulate counter to list
                    # print(accumulateCounter,"accumulateCounter")
                    accumulateList.append(accumulateCounter)
                    accumulateCounter = 1
                    curr = x
                else :
                    # No changes , accumulate reading
                    accumulateCounter += 1
        
        # Check
        for x in accumulateList :
            totalTime = self.calDuration(x)
            if totalTime >= fromTime and totalTime <= toTime :
                bolResult = True
        

        self.printConsole(data,fromTime,toTime,accumulateList,bolResult)
        return bolResult

    @helper_function.log_error()
    def SlowFlashing(self,data):
        # Capture the interval when light event occur
        # a. switch from on to off 
        # b. switch from off to on

        if not data : 
            return False
    
        fromTime = MQTTCON.SLOW_FLASH[0] * MQTTCON.MULTIPLIER
        toTime = MQTTCON.SLOW_FLASH[1] * MQTTCON.MULTIPLIER
        accumulateList = []
        accumulateCounter = 1
        bolResult = False

        # print(data,"data")
        curr = None
        for count,x in enumerate(data) :
            if curr == None :
                curr = x
            else :
                if x != curr :
                    # Detect changes , add accumulate counter to list
                    # print(accumulateCounter,"accumulateCounter")
                    accumulateList.append(accumulateCounter)
                    accumulateCounter = 1
                    curr = x
                else :
                    # No changes , accumulate reading
                    accumulateCounter += 1

            if count == len(data) - 1 :
                # Add counter to list for last element
                # skip 0 , above logic condition had added counter value 0
                if accumulateCounter != 0 :
                    accumulateList.append(accumulateCounter)

        # Check
        totalElement = len(accumulateList)
        for count,x in enumerate(accumulateList) : 
            if count + 2 > totalElement :
                # print("no more element")
                pass
            else :
                print(f"Comparing {accumulateList[count]} vs {accumulateList[count+1]}")
                totalTime = self.calDuration(accumulateList[count])
                totalTime2 = self.calDuration(accumulateList[count+1])

                # first half
                firstHalfResult = totalTime >= fromTime and totalTime <= toTime 
                secondHalfResult = totalTime2 >= fromTime and totalTime2 <= toTime 
                
                if secondHalfResult and firstHalfResult :
                    bolResult = True
                    print("result",bolResult)


        self.printConsole(data,fromTime,toTime,accumulateList,bolResult)
        return bolResult

    @helper_function.log_error()
    def FlashOffOnce(self,data):
        self.fromTime:float = MQTTCON.FLASH_OFF_ONCE[0] * MQTTCON.MULTIPLIER
        self.toTime :float = MQTTCON.FLASH_OFF_ONCE[1] * MQTTCON.MULTIPLIER
        self.PatternToCapture = cycle([LightEvent.SolidOn.value , LightEvent.SolidOff.value , LightEvent.SolidOn.value])
        return self.FlashOnceCommon(data)
        
    @helper_function.log_error()
    def FlashOnOnce(self,data):
        self.fromTime:float = MQTTCON.FLASH_ON_ONCE[0] * MQTTCON.MULTIPLIER
        self.toTime :float = MQTTCON.FLASH_ON_ONCE[1] * MQTTCON.MULTIPLIER
        
        pattern = [LightEvent.SolidOff.value , LightEvent.SolidOn.value , LightEvent.SolidOff.value]
        self.PatternToCapture = cycle(pattern)
        # print(pattern)
        result = self.FlashOnceCommon(data)
        # print(test,"Result")
    
        return result

    def FlashOnceCommon(self,data):
        ''' 
        FlashOffOnce -> Interval from on to off and from off to on must within range
        FlashOnOnce ->  Interval from off to on and on to off must within range 

        fromTime    : The minimum range of duration , pass from BE
        toTime      : The maximum range of duration , pass from BE

        accumulateCounter : To incre counter when same signal matched.
        patternToCapture : cycle iterable that contain 3 value for poping
        patternToCaptureCurrentValue : pattern value poped from patternToCapture , use during iterate data to validate pattern.
        currentIndexInPatternIterable : integer index to indicate whether current pattern is at index of 0 || 1 || 2 , max 2. Larger than 2 will reset to 0 to consider as a new session.

        patternCapturedCounter : tuple that contain 2 values e.g 112211 data produced (2,2) for FlashOffOnce function.
        patternCaptured : high level variable that store list of patternCapturedCounter
        
        '''

        if not data : 
            return False

        fromTime:float = self.fromTime
        toTime :float = self.toTime
        accumulateCounter : int = 0
        bolResult : bool = False
        patternToCapture : cycle[int] =  self.PatternToCapture
        patternToCaptureCurrentValue  :int = next(patternToCapture)
        currentIndexInPatternIterable : int = 0
    
        patternCapturedCounter: tuple[int,int] = ()
        patternCaptured : List[tuple[int,int]] = []

        previousPattern:int = None
        currentPattern:int = None # 1 or 2

        print(colored('Pattern','green'),self.PatternToCapture)


        def IsLast(totalLength:int,current:int):
            if (current + 1) == totalLength :
                return True
            return False

        def IsFullPatternMatchAndLegalCounter(currentIndexInPatternIterable:int):
            if currentIndexInPatternIterable == 2 :
                return True
            print(f"Index haven't reach last pattern , wont consider as a full pattern")
            return False

        def NextPattern():
            return next(patternToCapture)

        def PatternIndexReset(index:int):
            index += 1

            if index == 3 :
                return 0
            else :
                return index

        if data and len(data) > 0 :
            print(f"Input {data}")
            for counter, x in enumerate(data) :
                print(f"===== Iterating {x} , to match pattern {patternToCaptureCurrentValue}")
                if x == patternToCaptureCurrentValue :
                    accumulateCounter += 1
                    currentPattern = x
                    previousPattern = x
                    
                    print(f"Matched {x} pattern , Counter :{accumulateCounter} ")

                    # Check if last , add only if current is still accumulate
                    if IsLast(len(data),counter) and IsFullPatternMatchAndLegalCounter(currentIndexInPatternIterable) :
                        patternToCaptureCurrentValue = NextPattern()
                        currentIndexInPatternIterable = PatternIndexReset(currentIndexInPatternIterable)
                        
                     
                        patternCapturedCounter = patternCapturedCounter + (accumulateCounter,)
                        accumulateCounter = 1
                        print(f"Last element in iterable, append total accumulate counter to tuple {patternCapturedCounter}")  
                        
                        # New batch tuple
                        if len(patternCapturedCounter) == 2 :
                            
                            patternToCapture =  self.PatternToCapture
                            patternToCaptureCurrentValue= next(patternToCapture)
                            currentIndexInPatternIterable = PatternIndexReset(currentIndexInPatternIterable)
                            # print("Reset pattern cycle")

                        
                            patternCaptured.append(patternCapturedCounter)
                            patternCapturedCounter = ()
                            accumulateCounter = 1
                            # print("Add tuple to list and Reset tuple and counter ")

                            currentPattern = None
                            # print("Reset current pattern")
                            print("New batch tuple , reset all data.")
                else :
                    # Detect change , check next pattern in next loop , add accumulate counter to tuple
                    if currentPattern :
                        
                        # Append changes data
                        # accumulateCounter += 1
                        patternCapturedCounter = patternCapturedCounter + (accumulateCounter,)
                        msg = f"Detect change after {previousPattern}, counter:{accumulateCounter} append total accumulate counter to tuple {patternCapturedCounter}"

                        if MQTTCON.DEBUG: print(colored('Detect changes','green'),msg)   

                        # Reset , and check next pattern
                        patternToCaptureCurrentValue = NextPattern()
                        currentIndexInPatternIterable = PatternIndexReset(currentIndexInPatternIterable)
                        accumulateCounter = 1

                        if MQTTCON.DEBUG: print(f"Update next pattern {patternToCaptureCurrentValue} , reset counter to 1")   

                        # New batch tuple
                        if len(patternCapturedCounter) == 2 :
                         
                            patternToCapture =  self.PatternToCapture
                            patternToCaptureCurrentValue= NextPattern()
                            # print("Reset pattern cycle")
                  
                            patternCaptured.append(patternCapturedCounter)
                            patternCapturedCounter = ()
                            accumulateCounter = 0
                            # print("Add tuple to list and Reset tuple and counter ")

                            currentPattern = None
                            # print("Reset current pattern")
                            if MQTTCON.DEBUG: print("New batch tuple , reset all data.")
                    else :
                        # Must atleast obtain first pattern first.
                        if MQTTCON.DEBUG: print(f"Looping to Match first pattern.")
                        continue

                        
            # Check valid
            for x in patternCaptured :
                print(x)
                fromSignal , toSignal = x
                totalTime = self.calDuration(fromSignal)
                totalTime2 = self.calDuration(toSignal)

                firstHalfResult =  totalTime >= fromTime and totalTime <= toTime 
                secondHalfResult = totalTime2 >= fromTime and totalTime2 <= toTime 

                if secondHalfResult and firstHalfResult :
                    print(colored(f"Matched time range {totalTime},{totalTime2}",'green'))
                    bolResult = True
                else :
                    print(f"Not Match time range {totalTime},{totalTime2}")

        printData = dict(
            data = data ,
            patternCaptured = patternCaptured ,
            bolResult = bolResult,
            fromTime = fromTime ,
            toTime =toTime,
            # accumulateDuration = list(map(self.calDuration,patternCaptured)) ,
        )
        

        if MQTTCON.DEBUG: print(colored(f'Pattern Interval Result ','cyan'),printData)  

        return bolResult
        




# PV = PatternVariantInterval()

# print(PV.SolidOn([1]))
# print(PV.SolidOn(None))
# print(PV.SolidOn([]))
# print(PV.SolidOn([1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,2,2,2,1,1]))
# print(PV.SolidOn([1,1,1,1,1,2,2,2,2]))
# print(PV.SolidOn([1,1,1,1,2,2,2,2]))
# print(PV.SolidOn([1,1,1,1,2,2,2,2]))
# print(PV.SolidOn([1,1,1,2,2,2,2]))


# PV.FastFlashing(None)
# PV.FastFlashing([1])
# PV.FastFlashing([])
# PV.FastFlashing([1, 1, 1, 1, 1, 2, 2, 2, 2])
# PV.FastFlashing([1,1,2,2,2,2,2,1,1])
# PV.FastFlashing([1,1,2,2,1,1,2,2,1,1])
# PV.FastFlashing([2,2,2,2,2,1,1,1,1])

# PV.FastFlashing([1,2,1,2])
# PV.FastFlashing([1,2,2,1])
# PV.FastFlashing([1,2,2,2,2,2])
# PV.FastFlashing([1,2,2,2,2,2,1])

# PV.SlowFlashing(None)
# PV.SlowFlashing([1])
# PV.SlowFlashing([])
# PV.SlowFlashing([1, 1, 1, 1, 1, 2, 2, 2, 2])
# PV.SlowFlashing([1, 1, 1, 1, 1, 1,1,1,1,1,1,2])
# PV.SlowFlashing([2,2,2,2,2,2,2,2,2,2,1])
# PV.SlowFlashing([2,2,2,2,2,2,2,2,2,2,1,1,1, 1, 1, 1, 1,1,1,1,1,1,2])
# PV.SlowFlashing([1, 1, 1, 1, 1, 1,1,1,1,1,1,2,1,2,2,2,2,2,2,2,2,2,2,1,1,1, 1, 1, 1, 1,1,1,1,1,1,2])



# PV.FlashOffOnce(None)
# PV.FlashOffOnce([])
# PV.FlashOffOnce([1])
# PV.FlashOffOnce([1,1,2,1,1])
# PV.FlashOffOnce([1,1,1,2,1,2,2,1,1,2]) # expected (3,1) ,(2,1)
# PV.FlashOffOnce([2,2,2,2,1,1,2,1]) # expected (2,1)
# PV.FlashOffOnce([1,2,1,2,2,2,2,1]) # expected (1,1)


# PV.FlashOnOnce([1,1,2,1,1]) # expected (0,)
# PV.FlashOnOnce([1,1,2,2,2,2,2,1,1]) # expected (0,)
# PV.FlashOnOnce([2]) # expected (0,)
# PV.FlashOnOnce([2,2,2,1,2,2]) # expected (3,1)
# PV.FlashOnOnce([2,1,2,2,2,1,1,2,2]) # expected (1,1) (2,2)
# PV.FlashOnOnce([2,2,2,2,1,1,1,1,2,2,2,2,2]) # expected (4,2)