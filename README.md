# pcs-rasp
Backend services that targeted install on raspberry-pi. Collect data from i2c IO and publish to mqtt broker with specify topic. 


### Flow
1. Main thread : i2c connection and handler.
2. 2nd thread : mqtt client
3. 3rd thraed : mqtt message consumer

### Dependency between cross threaded flow
1. Mqtt establish connection and obtain setting from server.
2. i2c connection iterate and loop 3 or 4 or 5 rasp IO via i2c bus protocol to obtain message and dump into queue. 
3. i2c will skip iterate and loop IO until Mqtt successful obtain tower type or setting from server.
 
### Rules
1. Client rasp will only subscribe to the topic that belong to it mac addres
2. Server mqtt will subscribe all topic with wildcard "+" subscribe any topic matches a topic with single-level wildcard if it contains an arbitrary. Refer [MQTT TOPIC BEST PRACTICES](https://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices/)

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

    > Listen topic via terminal  / cmd
        cd to mosquitto installed path

        e.g mosquitto_sub -h url -t topic
        e.g mosquitto_sub -h 127.0.0.1 -t 0x106530ea239e/server/config

    > Publish topic via terminal / cmd
        e.g mosquitto_pub -h 127.0.0.1 -t 0x106530ea239e/server/config -m "{\"test message\" : 1}" -d
    
   
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
    


