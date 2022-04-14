from __future__ import annotations
import time ,datetime
import os
from app.IOConnectionManager.i2c_singleton import I2CConfiguration
from app.IOConnectionManager.mock_i2c import mockData
from app.IOMQTT.mqtt_singleton import MQTTConfiguration
from app.Utilities.helper_function import getTowerColorGroup
from app.enum_type import LightEvent
from termcolor import colored


MQTTCON = MQTTConfiguration().instance
I2CCON = I2CConfiguration().instance
DEV = I2CCON.BOL_MOCK_IO 

if os.name == 'nt' and DEV == False :
    print("WINDOW OS - Skip import smbus due to Tthe fcntl module is not available on Windows")
else :
    if DEV == False :
        from smbus2 import SMBus
    

from app.EventManager import StateServices, towerToData

def i2c_connection(stateServices : StateServices):
    print("Thread i2c starting.")
    readi2c()

# https://www.electronicwings.com/raspberry-pi/python-based-i2c-functions-for-raspberry-pi
#  I2C port no. i.e. 0 or 1
i2c_ch = 1

# address on the I2C bus
i2c_address = 0x23

# Register addresses
reg_20 = 0x20
reg_21 = 0x21
reg_22 = 0x22
reg_23 = 0x23
reg_24 = 0x24
reg_25 = 0x25
reg_26 = 0x26
reg_27 = 0x27

reg_config = 0x01

def readi2c():
    ''' e.g reading value from i2c protocol for tower light device.
    
    Tower (3 type)
    Address 0x01 = 251 Green
    Address 0x01 = 249 Orange + Green
    Address 0x01 = 253 Orange
    Address 0x01 = 252 Red + Orange
    Address 0x01 = 254 Red
    Address 0x01 = 250 Red + Green
    Address 0x01 = 248 All On
    Address 0x01 = 255 all Off
    '''
    if DEV == False :
        bus1 = SMBus(1)
    time.sleep(2)
    bytesList = bytes([0x01])
    # bytesList = bytes([0x00, 0x01, 0x02, 0x03, 0x04, 0x05,0x06, 0x07, 0x08, 0x09, 0x10, 0x11,
    #              0x12, 0x13, 0x14, 0x15, 0x16, 0x17,0x18, 0x18, 0x19, 0x20, 0x21, 0x22,
    #                    0x23, 0x24,0x25, 0x26,0x27, 0x28])

    # 21 reset the counter 
    sessionData = []
    sessionCountLimit = MQTTCON.LIMIT_FREQUENCY # 20 = Total duration 2 seconds if frequency is 0.1
    currentSessionCounter = 1
    intFrequency = MQTTCON.FREQUENCY
    mockCount = 1
    rawData = []

    while True :
        try :
            if MQTTCON.TOWER_TYPE is not None :
                _towerAddress = tuple(getTowerColorGroup(MQTTCON.TOWER_TYPE))
                if currentSessionCounter > sessionCountLimit :
                    # Add to queue then reset.
                    if sessionData != [] :
                        data = dict(data = sessionData ,address = _towerAddress )
                        print(colored(f'{datetime.datetime.now()} i2c Raw Incoming','cyan'),f"{rawData} , len={len(rawData)}")
                        I2CCON.MESSAGE_QUEUE.put(data)
                        # print("put data in queue", data)
                        currentSessionCounter = 1  
                        sessionData = []
                        rawData = []
                        # print("Reset counter and empty data")
                else :
                    for x in bytesList :
                        try :
                            if DEV == False :
                                data = bus1.read_byte_data(i2c_address,x)
                                # print(f"Read Device Address:{i2c_address},Register Address:{x}, Data:{data}")
                            else :
                                data = mockData(LightEvent.SolidOff,mockCount)
                                mockCount +=1 

                            
                            rawData.append(data)
                                     
                            # print(MQTTCON.TOWER_TYPE,"This is tower type")
                            output = towerToData.towerType(MQTTCON.TOWER_TYPE,int(data))
                            # print(f"Output towerToData.towerType() {output}")

                            data_list = tuple(output)
                            sessionData.append(data_list)
                        
                            currentSessionCounter +=1
                        except Exception as e :
                            print(e)
                            continue
                                
            time.sleep(intFrequency)

        except OSError as e :
            time.sleep(10)
            msg =f"{datetime.datetime.now()} {e.args} Remote I/O error." \
            "An I2C device is not connected to the bus." \
            "Make sure that the sensors and micro OLED are securely connected to the I2C bus."
            print(msg)


def initialize_i2c():
  

    # Calculate the 2's complement of a number
    def twos_comp(val, bits):
        if (val & (1 << (bits - 1))) != 0:
            val = val - (1 << bits)
        return val
    # Initialize I2C (SMBus)
    bus = SMBus(i2c_ch)

    # Read the CONFIG register (2 bytes)
    val = bus.read_i2c_block_data(i2c_address, reg_config, 2)
    print("Old CONFIG:", val)

    # Set to 4 Hz sampling (CR1, CR0 = 0b10)
    val[1] = val[1] & 0b00111111
    val[1] = val[1] | (0b10 << 6)

    # Write 4 Hz sampling back to CONFIG
    bus.write_i2c_block_data(i2c_address, reg_config, val)

    # Read CONFIG to verify that we changed it
    val = bus.read_i2c_block_data(i2c_address, reg_config, 2)
    print("New CONFIG:", val)

    # Print out temperature every second
    while True:
        temperature = read_temp()
        print(round(temperature, 2), "C")
        time.sleep(1)
