

from typing import List
from app.enum_type import TowerType, TowerTypeColor


def towerType(towerType:int , readValue :int):
    if towerType == TowerTypeColor.One.value :
        return type1valueToColor(readValue=readValue)
    elif towerType == TowerTypeColor.Two.value :
        return type2valueToColor(readValue=readValue)
    elif towerType == TowerType.Three.value :
        return type3valueToColor(readValue=readValue)
    elif towerType == TowerType.Four.value :
        pass
    elif towerType == TowerType.Five.value :
        pass


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
