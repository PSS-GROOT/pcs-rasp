'''
# A variable to hold the state of the Tower IO

# Function Requirements
# 1. detectChanges() To detect changes of the tower light , Accept empty parameter to indicate the IO din't have 
#    any changes. (IO prompt change only if signal raise) if so then inform server by adding to queue , mqtt_services will emit.
# 2. intervalInform() Inform server within an interval (in seconds).
# 3. stateChangeAppendQueue() Queue that store the message related to event light change
# 4. serviceIOChangeAppendQueue() Queue that store the message related to service io change
 
'''


from datetime import datetime
import json
from typing import List

from termcolor import colored
from app.IOMQTT.mqtt_singleton import MQTTConfiguration
from app.enum_type import EventChangeType, ServiceStatus

MQTTCON = MQTTConfiguration().instance

class EventState:
    def __init__(self, eventArray , eventDetailed, unzipped_list) -> None:
        self.EventLightArray = eventArray
        self.EventLightDetailed = eventDetailed
        self.EventSignalData = self.joinList(unzipped_list)

    def __repr__(self) -> str:
        ''' e.g 
        {
            "EventLightArray": [2, 1, 2],
            "EventLightDetailed": {
                "Red": { "type": "SolidOff", "code": 2 }, 
                "Amber": {"type": "SolidOff", "code": 2}, 
                "Green": {"type": "SolidOn", "code": 1}}
            "EventSignalData" :{

            }
        } 

        '''
        # data = {
        #     'EventLightArray' : self.EventLightArray ,
        #     'EventLightDetailed' : self.EventLightDetailed
        # }
        return json.dumps(self.__dict__)

        
    def joinList(self,unzipped_list):
        newX = []
        for x in unzipped_list :
            string_ints = [str(int) for int in list(x)]
            str_of_ints = "". join(string_ints) 
            newX.append(str_of_ints)
        return newX



class StateServices():
    def __init__(self) -> None:
        self.currentEventLightState : EventState = None
        self.currentServiceState = ServiceStatus.Inactive.value   
        self.dateTimeLastInform = None

    @property
    def currentEventStateQty(self):
        if self.currentEventLightState :
            return len(self.currentEventLightState)
        else :
            pass

    def transfromToArray(self, incomingChange)-> List[int]:
        try :
            incomingChange = sorted(incomingChange.items())

            eventArray = []
            for k,v in incomingChange :
                # print(f"k {k}, v {v}")
                eventArray.append(v['code'])
                # print(eventArray)

            return eventArray
        except Exception as e :
            pass

        


    def detectChanges(self, incomingChange,unzipped_list) :
        #e.g incomingChange = 
        #   {
        #       'port1': {'type': 'SolidOff', 'code': 2}, 
        #       'port2': {'type': 'SolidOff', 'code': 2}, 
        #       'port3': {'type': 'SolidOn', 'code': 1}
        #   }

        try :
            if self.currentEventLightState is None :
                print("Default event is None , will update to state to StateService")

                self.currentEventLightState = EventState(self.transfromToArray(incomingChange),incomingChange,unzipped_list)
                self.eventLightChangeAppendQueue(EventChangeType.Passive)
                self.dateTimeLastInform = datetime.now()
            else :
                # print(f"Default is {self.currentEventLightState} , will compare the state between StateService and latest update from I2C")
            
                # Check len of both array
                incomingArray = self.transfromToArray(incomingChange)
                incomingArrayLength = len(incomingArray)
                existingArrayLength = len(self.currentEventLightState.EventLightArray) 
                
                # print(incomingArrayLength,'incomingArrayLength')
                # print(existingArrayLength,'existingArrayLength')

                requirePush = False
                msg = ''

                if incomingArrayLength == existingArrayLength :

                    # Validate identical
                    for x,y in zip(incomingArray,self.currentEventLightState.EventLightArray):
                        # print(x,y)
                        msg = "Signal identical , no changes from IO."
                        if x != y :
                            # Require push update
                            requirePush = True
                            msg = "Signal not identical , got changes from IO."

                else :
                    # Require push update to server
                    msg = "Signal len not tally, got changes from IO."
                    requirePush = True


                if requirePush :
                    # Require push update to server
                    print(colored(f'{datetime.now()} Push Event Update','cyan'),f"{msg}")
                    self.currentEventLightState = EventState(self.transfromToArray(incomingChange),incomingChange,unzipped_list)
                    self.eventLightChangeAppendQueue(EventChangeType.Passive)
                    self.dateTimeLastInform = datetime.now()
                else :
                    print(colored(f'{datetime.now()} Push Event Update','cyan'),f"Detected tower light state remain , wont push update to server.")                   
        except Exception as e :
            MQTTCON.addErrorMessage(e.args)



                
                

    def eventLightChangeAppendQueue(self, changeType : EventChangeType):
        try :
            if self.currentEventLightState :
                MQTTCON.SEND_MESSAGE_QUEUE.put([self.currentEventLightState,'/client/event',changeType.value])
                self.dateTimeLastInform = datetime.now()
        except Exception as e :
            MQTTCON.addErrorMessage(e.args)

    def serviceIOChangeAppendQueue(self):
        try :
            MQTTCON.SEND_MESSAGE_QUEUE.put([self.currentServiceState,'/client/service', None])
        except Exception as e :
            MQTTCON.addErrorMessage(e.args)

    def intervalInform(self):
        try :
            if MQTTCON.BOL_INTERVAL_UPDATE :
                if self.dateTimeLastInform is None :
                    self.dateTimeLastInform = datetime.now()

                totalElapse =   datetime.now() - self.dateTimeLastInform
                if totalElapse.seconds > MQTTCON.INTERVAL_UPDATE :
                    
                    #Push update to server
                    self.eventLightChangeAppendQueue(EventChangeType.Active)
                    
            else :
                # Feature is turned off , wont emit.
                pass
        except Exception as e :
            MQTTCON.addErrorMessage(e.args)


    
        