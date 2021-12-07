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

class LightEvent(Enum):
    ''' Use by repo pcs-rasp '''
    # There are six major light event for each color, every color can have 6 combination of lighting type either in flashing or continuous.
    SolidOn = 1             # 点灯      |||||||||||||||
    SolidOff = 2            # 消灯      xxxxxxxxxxxxxxx
    FastFlashing = 3        # 高速点灭  |x|x|x|x|x|x|x|
    SlowFlashing = 4        # 低速点灭  ||xx||xx||xx|||
    DUNKNOW = 5             # 瞬时点灯  x|xxxxxxxxxxxxx
    DUNKNOW2 = 6            # 瞬时消等  |x|||||||||||||  


class ColorType(Enum):
    ''' Use by repo pcs-rasp '''
    # The color code follow the order of the actual tower light , from top to down.
    Red = 1 
    Amber = 2
    Green = 3
    Blue = 4
    White = 5


