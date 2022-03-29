from __future__ import annotations
import time
import os
from app.IOConnectionManager.i2c_singleton import I2CConfiguration
from app.IOMQTT.mqtt_singleton import MQTTConfiguration
from smbus2 import SMBus

MQTTCON = MQTTConfiguration().instance
I2CCON = I2CConfiguration().instance

# if os.name == 'nt':
#     print("WINDOW OS - Skip import smbus due to Tthe fcntl module is not available on Windows")
# else :
#     import smbus2 as smbus
    

from app.EventManager import StateServices

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
    bus1 = SMBus(1)

    while True :
        intFrequency = MQTTCON.FREQUENCY

        # Read temperature registers
        val20 = bus1.read_i2c_block_data(i2c_address, reg_20, 2)
        val21 = bus1.read_i2c_block_data(i2c_address, reg_21, 2)
        val22 = bus1.read_i2c_block_data(i2c_address, reg_22, 2)
        val23 = bus1.read_i2c_block_data(i2c_address, reg_23, 2)
        val24 = bus1.read_i2c_block_data(i2c_address, reg_24, 2)
        val25 = bus1.read_i2c_block_data(i2c_address, reg_25, 2)
        val26 = bus1.read_i2c_block_data(i2c_address, reg_26, 2)
        val27 = bus1.read_i2c_block_data(i2c_address, reg_27, 2)
    
        print(val20,'0x20')
        print(val21,'0x21')
        print(val22,'0x22')
        print(val23,'0x23') 
        print(val24,'0x24')
        print(val25,'0x25')
        print(val26,'0x26')
        print(val27,'0x27')

        # data = dict(data = temp_data ,address = ('port1','port2','port3') )

        # I2CCON.MESSAGE_QUEUE.put(data)

        time.sleep(1)


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
