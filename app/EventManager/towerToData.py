
from typing import List
from app.enum_type import TowerType, TowerTypeColor


def towerType(towerType:int , readValue :int):
    ''' 
    Return list of int 
        e.g [1,1,1]
    '''
    if towerType == TowerType.One.value :
        return type1valueToColor(readValue=readValue)
    elif towerType == TowerType.Two.value :
        return type2valueToColor(readValue=readValue)
    elif towerType == TowerType.Three.value :
        return type3valueToColor(readValue=readValue)
    elif towerType == TowerType.Four.value :
        return type4valueToColor(readValue=readValue)
    elif towerType == TowerType.Five.value :
        return type5valueToColor(readValue=readValue)


def type3valueToColor(readValue:int)-> List[int]:
    # Three = ["Red","Amber","Green"]
    # off = 2
    # on = 1
    if readValue == 248 :
        return [1,1,1]
    elif readValue == 249 : 
        return [2,1,1]
    elif readValue == 250 : 
        return [1,2,1]
    elif readValue == 251 : 
        return [2,2,1]
    elif readValue == 252 : 
        return [1,1,2]
    elif readValue == 253 : 
        return [2,1,2]
    elif readValue == 254 : 
        return [1,2,2]
    elif readValue == 255 : 
        return [2,2,2]
    else :
        return [3,3,3]


def type2valueToColor(readValue:int)-> List[int]:
    # Two = ["Red","Amber"]
    # off = 2
    # on = 1
    if readValue == 252 : 
        return [1,1]
    elif readValue == 253 : 
        return [2,1]
    elif readValue == 254 : 
        return [1,2]
    elif readValue == 255 : 
        return [2,2]
    else :
        return [3,3,3]

def type1valueToColor(readValue:int) -> List[int]:
    # One = ["Red"]
    # off = 2
    # on = 1
    if readValue == 254 :
        return [1]
    if readValue == 255 : 
        return [2]
    else :
        return [3,3,3]

def type4valueToColor(readValue:int) -> List[int]:
    # Not implemented , return Unknown value
    return [3,3,3,3]

def type5valueToColor(readValue:int) -> List[int]:
    # Return 
    if readValue == 224 :
        return [1,1,1,1,1]
    if readValue == 225 : 
        return [2,1,1,1,1]
    if readValue == 226 :
        return [1,2,1,1,1]
    if readValue == 227 : 
        return [2,2,1,1,1]
    if readValue == 228 :
        return [1,1,2,1,1]
    if readValue == 229 : 
        return [2,1,2,1,1]
    if readValue == 230 :
        return [1,2,2,1,1]
    if readValue == 231 : 
        return [2,2,2,1,1]
    if readValue == 232 : 
        return [1,1,1,2,1]
    if readValue == 233 : 
        return [2,1,1,2,1]
    if readValue == 234 : 
        return [1,2,1,2,1]
    if readValue == 235 : 
        return [2,2,1,2,1]
    if readValue == 236 : 
        return [1,1,2,2,1]
    if readValue == 237 : 
        return [2,1,2,2,1]
    if readValue == 238 :
        return [1,2,2,2,1]
    if readValue == 239 : 
        return [2,2,2,2,1]
    if readValue == 240 : 
        return [1,1,1,1,2]
    if readValue == 241 : 
        return [2,1,1,1,2]
    if readValue == 242 : 
        return [1,2,1,1,2]
    if readValue == 243 : 
        return [2,2,1,1,2]
    if readValue == 244 : 
        return [1,1,2,1,2]
    if readValue == 245 : 
        return [2,1,2,1,2]
    if readValue == 246 : 
        return [1,2,2,1,2]
    if readValue == 247 : 
        return [2,2,2,1,2]
    if readValue == 248 : 
        return [1,1,1,2,2]
    if readValue == 249 : 
        return [2,1,1,2,2]
    if readValue == 250 : 
        return [1,2,1,2,2]
    if readValue == 251 : 
        return [2,2,1,2,2]
    if readValue == 252 : 
        return [1,1,2,2,2]
    if readValue == 253 : 
        return [2,1,2,2,2]
    if readValue == 254 : 
        return [1,2,2,2,2]
    if readValue == 255 : 
        return [2,2,2,2,2]
    else :
        return [3,3,3,3,3]
