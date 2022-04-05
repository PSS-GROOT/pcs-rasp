import functools
from json import JSONEncoder
import datetime
from typing import List
from app.enum_type import TowerType, TowerTypeColor

class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()


    
def getTowerColorGroup(tower_type: int)-> List[str]:
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
        if tower_type == 1 :
            tower_type = TowerType.One
        elif tower_type == 2 :
            tower_type = TowerType.Two
        elif tower_type == 3 :
            tower_type = TowerType.Three
        elif tower_type == 4 :
            tower_type = TowerType.Four
        elif tower_type == 5 :
            tower_type = TowerType.Five

        colors = TowerTypeColor[tower_type.name] 
        # print(colors)         
        return colors.value
    except Exception as e :
        print(e.args)



def log_error():
    def argument_decorator(original_function):
        @functools.wraps(original_function)
        def decorated_function(*args, **kwargs):
            try:
                return original_function(*args, **kwargs)
            except Exception as e:
                print(
                    f"During execution of "
                    f"{original_function.__qualname__} with postional "
                    f"argument(s) {args}, and keyword argument(s) {kwargs}, "
                    f"{repr(e)} was raised.")
        return decorated_function
    return argument_decorator