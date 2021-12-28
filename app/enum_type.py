from enum import Enum

class PublishTopic(Enum):
    Config = "/server/config"
    Ping = "/server/ping"
    ConfigUpdate = "/server/config/update"

class ClientPublishTopic(Enum):
    RequestConfig = "/client/config"
    ReplyService = "/client/service"
    ReplyEvent = "/client/event"
    ReplyErrorLog = "/client/error"

class TowerType(Enum):
    ''' Use by repo pcs-rasp '''
    # There are total 5 towers type from 1 color to maximum 5 colors
    One = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5

class TowerTypeColor(Enum):
    # Each tower type map to specific color , or can iterate with enum ColorType according to TowerType's quantity
    One = ["Red"]
    Two = ["Red","Amber"]
    Three = ["Red","Amber","Green"]
    Four = ["Red","Amber","Green","Blue"]
    Five = ["Red","Amber","Green","Blue","White"]

class LightEvent(Enum):
    ''' Use by repo pcs-rasp '''
    # There are six major light event for each color, every color can have 6 combination of lighting type either in flashing or continuous. There are total 7776 combinations for six event lights with five colors and it can denote as : 6*6*6*6*6*6
    SolidOn = 1             # 点灯      |||||||||||||||
    SolidOff = 2            # 消灯      xxxxxxxxxxxxxxx
    FastFlashing = 3        # 高速点灭  |x|x|x|x|x|x|x|
    SlowFlashing = 4        # 低速点灭  ||xx||xx||xx|||
    FlaskOnOnce = 5         # 瞬时点灯  x|xxxxxxxxxxxxx
    FlaskOffOnce = 6        # 瞬时消灯  |x|||||||||||||  
    Unknown = 0


class ColorType(Enum):
    ''' Use by repo pcs-rasp '''
    # The color code follow the order of the actual tower light , from top to down.
    Red = 1 
    Amber = 2
    Green = 3
    Blue = 4
    White = 5

class EventDesc(Enum):
    Running = 1         #Green solid on and other SolidOff
    Warning = 2         #Amber solid on and other Solidoff   || Amber on , green on || Ambet on , green in [2,3,4,5]
    Alert = 3           #Red solid on and other Solidoff  
    Down = 5            # All off