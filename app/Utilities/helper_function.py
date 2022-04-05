from json import JSONEncoder
import datetime
from typing import List

from app.enum_type import TowerType, TowerTypeColor

class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()


    
def getTowerColorGroup(tower_type: TowerType)-> List[str]:
    ''' 
        #Returns List[str]

        #Parameters:
            tower_type(TowerType) :  TowerTower enum instance
        
        #Return:
            List[str] : Return enum value e.g ['Red', 'Amber', 'Green', 'White'] 
    '''
    try :
        # e.g tower_type.name = Five
        # colors = ['Red', 'Amber', 'Green', 'White'] 
        colors = TowerTypeColor[tower_type.name]            
        return colors.value
    except Exception as e :
        print(e.args)
