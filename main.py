import test
from app.IOConnectionManager import i2c_client
from app.IOMQTT import mqtt_client , mqtt_services
from concurrent.futures import ThreadPoolExecutor
import threading
from uuid import getnode as get_mac
import sys

executor = ThreadPoolExecutor(2)



def backgroundTask(client_id):
    executor.submit(mqtt_client.init_client(type='client',name='pcs-rasp',client_id=client_id))
    executor.submit(mqtt_services.mqtt_consumer())


if __name__ == "__main__" :
    try :
        if len(sys.argv) == 2:
            # Invoke with argument , probably is simulation.
            client_id = sys.argv[1]
            print(client_id)

        elif len(sys.argv) == 1 :
            # Invoke without argument , probably is production mode with real rasp.
            client_id = hex(get_mac())

        backgroundTask(client_id)
        i2c_client.i2cModule()

    except Exception as e :
        print(e.args)
   
