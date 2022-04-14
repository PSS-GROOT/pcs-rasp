from dotenv import load_dotenv
import os 

load_dotenv()  # take environment variables from .env.
env = os.getenv('ENVIRONMENT')

if env == 'DEVELOPMENT':
    MQTT_HOST = os.environ.get("DEV_MQTT_HOST")

elif env == 'PRODUCTION' : 
    MQTT_HOST = os.environ.get("PROD_MQTT_HOST")
    print(MQTT_HOST)

elif env == "TEST" :
    pass

DEBUG = os.environ.get('DEBUG',False)