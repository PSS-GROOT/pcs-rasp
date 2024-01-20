# pcs-rasp
Backend services that targeted install on raspberry-pi. Collect data from i2c IO and publish to mqtt broker with specify topic. 

### Usage (Server must got the record for every device and able to response setting)
1. For single device simulation run > python main.py
2. For multiple device simulation , edit configureMock.py and run > python configureMock.py (device mac address mock from integer 1 and increment by 1 for next device.)

### Thread
1. Main thread : i2c connection and handler.
2. 2nd thread : mqtt client
3. 3rd thraed : mqtt message consumer

### Functional Requirement
1. Rasp establish MQTT connection and auto perform reconnection when broker down.
2. Rasp request setting and auto reattempt when no response after exceed timeout.
3. Rasp update configuration to singleton variable upon receive response from server.
4. Rasp use modbus to establish i2c connection with raspberry IO.
5. Rasp implement busy loop pattern and read i2c bus protocol to obtain tower light signal.
6. Rasp read IO based on tower type and processes the data.
7. Rasp update tower light event to server upon detected changes.
    > Answer : rasp will auto detect , in app.EventManager.state_services.py
8. Rasp update tower light event to server in fix interval.
    > Answer : can set in app.IOMQTT.mqtt_singleton.py
9. Rasp apply time out setting (in Seconds) to limit the time for running. (When to resume ?)
    > Answer :

 
### Rules of Thumb
1. Client rasp will only subscribe to the topic that belong to its own mac address
2. Server MQTT will subscribe all topic with wildcard "+" subscribe any topic matches a topic with single-level wildcard if it contains an arbitrary. Refer [MQTT TOPIC BEST PRACTICES](https://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices/)

### File structure
    .
    ├── github                      # Contain github ci/cd workflows
        |── workflows               # Contain YAML file
    ├── app                         # Main app folder
        |── IO.ConnectionManager    # Contain i2c connection or other connection to rasp IO board
        |── IO.MQTT                 # Contain mqtt connection and event
        |── Utilities               # Contain other utility and helper functions 
    ├── tests                       # unit test , integration test and e2e test
    ├── docs                        # Documentation
    ├── main.py                     # Driver code
    ├── README.md
    ├── requirements.txt
    ├── .env_sample
    └── .gitignore

### Installation
1. Tools and software
- Mosquitto Mqtt
    > Download [Mosquitto](https://mosquitto.org/download/)
    > For Local windowOS, ensure the broker is running under services.msc
    > For mock raspberry device, run at terminal 
    > For network broker, mosquitto installed at machine .171

        python -m app.mqtt.mqtt_mock_rasp {client_id:int}
        python -m app.mqtt.mqtt_mock_rasp 1234

    1. Example request config to rasp-be via MQTT:

    ![PCS-RASP-CONFIG](docs/MQTT_CLIENT_CONFIGURATION_PROTOCOL.png)


    2. Example output to rasp-be via MQTT :

    ![PCS-RASP-OUTGOING](docs/MQTT_CLIENT_TOWEREVENT_PROTOCOL2.png)


    > Listen topic via terminal  / cmd
        cd to mosquitto installed path

        e.g mosquitto_sub -h url -t topic
        e.g mosquitto_sub -h 127.0.0.1 -t 0x106530ea239e/server/config
        e.g mosquitto_sub -h 191.168.0.171 -t 0x106530ea239e/client/event

    > Publish topic via terminal / cmd
        e.g mosquitto_pub -h 127.0.0.1 -t 0x106530ea239e/server/config -m "{\"tower_type\" : 1}" -d
        e.g mosquitto_pub -h 127.0.0.1 -t 0x106530ea239e/server/ping -m "{\"status\" : 1}" -d
        e.g mosquitto_pub -h 127.0.0.1 -t 0x106530ea239e/server/config/update -m "{\"frequency\" : 1}" -d
    
   
2. Activate virtual environment and install dependencies
- pip install virtualen

    Window OS
    > py -m virtualenv venv *OR* python -m virtualenv venv OR py -m venv venv
    > tc\Scripts\activate   
    > pip install -r requirements.txt   

    Linux || macOS
    > virtualenv tc     
    > source tc/bin/activate    
    > pip install -r requirements.txt 

3. Create .env file
- create .env at root directory , refer .env_sample

4. Run unittest 
-  python -m unittest discover -s tests -p "test_*.py" -v

5. Practices & Format
- Date time format [ISO8601](https://www.iso.org/iso-8601-date-and-time-format.html)

6. Resources
    - https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial/all#i2c-on-pi
    - https://www.tomshardware.com/how-to/back-up-raspberry-pi-as-disk-image
    - https://stackoverflow.com/questions/190010/daemon-threads-explanation
    - https://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices/
    - https://www.dummies.com/article/technology/programming-web-design/python/
    - https://www.dummies.com/article/technology/programming-web-design/python/what-is-i2c-python-programming-basics-for-the-raspberry-pi-264864
    - https://learn.sparkfun.com/tutorials/python-programming-tutorial-getting-started-with-the-raspberry-pi/experiment-4-i2c-temperature-sensor
    - https://raspberry-projects.com/pi/programming-in-python/i2c-programming-in-python/using-the-i2c-interface-2
    - https://www.c3controls.com/white-paper/selecting-installing-tower-lights/
    

7. To run simulation in batch
    > Configure BOL_MOCK_IO to True at i2c_singleton.py
    > python configureMock.py


8. To enable i2c on raspberry
    > sudo raspi-config
    > select 5 Interfacing Options
    > select P5 I2C

9. To see all the connected devices
    > sudo i2cdetect -y 1


10. Publisher
    MacOS
    1. Run mqtt with terminal
    > /opt/homebrew/opt/mosquitto/sbin/mosquitto -c /opt/homebrew/etc/mosquitto/mosquitto.conf -v

    2. Publish event msg
    > mosquitto_pub -h localhost -t "1/client/event" -m "{\"user\":"nickson"}"
    
    3. Publish config msg
    > mosquitto_pub -h localhost -t "1/server/config" -m "{\"frequency\": 10, \"client_id\": 75, \"tower_type\": 3, \"reconnect_interval\": 15, \"interval_update\": 30 , \"retention_day\": 7 , \"retention_gb\" : 5  }"

