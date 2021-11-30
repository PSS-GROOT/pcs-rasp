# pcs-rasp
Backend services that communicate with backend server.

[Doc cloud link password:PSS](https://whimsical.com/pcs-UUWPYTmjdTin3tQacjEDCj)

### File structure
.
├── github                   # Contain github ci/cd workflows 
    |── workflows            # Contain YAML file
├── app                      # Main app folder
├── tests                    # unit test , integration test and e2e test
├── docs                     # Documentation
├── main.py                  # Driver code
├── README.md
├── requirements.txt
├── .env_sample
└── .gitignore

### Installation
1. Tools and software
- Mosquitto Mqtt
    > Download [Mosquitto](https://mosquitto.org/download/)
    > For windowOS, ensure the broker is running under services.msc
    > For mock raspberry device, run at terminal 

        python -m app.mqtt.mqtt_mock_rasp {client_id:int}
        python -m app.mqtt.mqtt_mock_rasp 1234

    > Listen topic via terminal  / cmd
        cd to mosquitto installed path

        e.g mosquitto_sub -h url -t topic
        e.g mosquitto_sub -h 127.0.0.1 -t 0x106530ea239e/server/config
    
   
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

5. Other
- freeze requirement 'pip freeze > requirements.txt'
- cuztomize f5 debug file and point to main.py , open your launch.json
    >  "program": "${workspaceFolder}/main.py",
- git squash last n commit
    > git reset --soft HEAD~3 &&  git commit

6. Remark
- No logging services to prevent hard disk overflow.