from app.IOConnectionManager import i2c_client
from app.IOMQTT import mqtt_client , mqtt_services
from concurrent.futures import ThreadPoolExecutor
from uuid import getnode as get_mac
import sys
from app.Utilities import sqlite

executor = ThreadPoolExecutor(3)



def backgroundTask(client_id):
    executor.submit(mqtt_client.init_client(type='client',name='pcs-rasp',client_id=client_id))
    executor.submit(mqtt_services.mqtt_consumer())
    executor.submit(sqlite.create_thread())

def getserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR000000000"
 
  return cpuserial


if __name__ == "__main__" :
    try :
        if len(sys.argv) == 2:
            # Invoke with argument , probably is simulation.
            client_id = sys.argv[1]
            print(f"invole with argument 1 {client_id}")

        elif len(sys.argv) == 1 :
            # Invoke without argument , probably is production mode with real rasp.
            #client_id = hex(get_mac())
            client_id = getserial()

        backgroundTask(client_id)  
        i2c_client.i2cModule()

    except Exception as e :
        print(e.args)
   
