
import json
import os
import sqlite3
from datetime import datetime, timedelta
from threading import Thread
from typing import List, Tuple
import time

from app.IOMQTT import mqtt_client


def create_thread():
    loop_start = Thread(target=RaspSqlite.connect, args=())
    loop_start.setName('sqlite')
    loop_start.daemon = True
    loop_start.start()

class RaspSqlite:
    conn: sqlite3.Connection = None
    cursor: sqlite3.Cursor = None
    ready: bool = False
    rows: List[Tuple[str,str]] = [] # queue for external module to store all the data to persist, loop() will store to database

    config_rows = []

    persist_max_gb:int = 5
    persist_days:int = 7

    @classmethod
    def max_rows(cls):
        # Per gb can store up to 775573 messages 
        # where 775573 = 1gb / 1352 bytes
        return int(cls.persist_max_gb * 775573)
    

    @classmethod
    def connect(cls):
        try :
            database_file_path = os.path.join(os.getcwd(), "mqtt_data.db")
            cls.conn = sqlite3.connect(database_file_path)
            cls.cursor = cls.conn.cursor()
            cls.ready = True
            cls.create_table()
            cls.retrieve_config()

            cls.loop()

        except Exception as e :
            cls.ready = False
            print(f"Exception Sqlite connect() {str(e.args)}")

    @classmethod
    def loop(cls):
        # Persist data to sqlite
        # Resend persist data if mqtt connected
        # Save config to sqlite

        while True and cls.ready :
            data = cls.rows.copy()
            for row in data :
                payload , dtString = row
                cls.store(payload,dtString)
    
            config_data = cls.config_rows.copy()
            for row in config_data :
                cls.update_config(row)

            cls.rows.clear()
            cls.config_rows.clear()          
            time.sleep(0.5)

            if mqtt_client.connected :
                from app.IOMQTT.mqtt_services import MqttServices
                current_row = cls.select_count()

                if current_row :
                    rows = cls.retrieve_data()
                    start = datetime.now()
                    for data in rows :
                        payload , dt = data
                        MqttServices.retry_persist_data(payload)
                    print(f"Total {len(rows)} row synced, elapsed in seconds : {(datetime.now() - start).total_seconds()}")
                    cls.clear_data()

    @classmethod
    def create_table(cls):
        if cls.ready :
            cls.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS mqtt_outgoing (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payload TEXT,
                dt TEXT  -- Storing datetime as ISO 8601 formatted string
            );

            """
        )
            
            cls.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payload TEXT,
                dt TEXT  -- Storing datetime as ISO 8601 formatted string
            );

            """
            )
    
    @classmethod
    def retrieve_config(cls):
        try :
            if cls.ready:
                cls.cursor.execute("SELECT payload,dt FROM config")
                result = cls.cursor.fetchall()
                for r in result :
                    config , dt = r 
                    config_obj = json.loads(config)
                    cls.persist_days = config_obj.get("retention_day",7)
                    cls.persist_max_gb = config_obj.get("retention_gb",5)
                    print(f"Retrieve config from {config}")

        except Exception as e :
            print(f"sqlite.py retrieve_config() Exception {e.args}")
    
    @classmethod
    def update_config(cls,payload):
        if cls.ready:
            cls.cursor.execute("Delete FROM config")
            cls.conn.commit()
            
            cls.cursor.execute(
                """
            INSERT INTO config (
                payload, dt
            ) VALUES (?, ?)
            """,
            (
                payload,
                datetime.now().isoformat(),
            ),
            )
            cls.conn.commit()

            
    @classmethod
    def retrieve_data(cls) -> List[Tuple[str, str]]:
        if cls.ready:
            # since_date = datetime.now() - timedelta(days=cls.persist_days)
            # since_date = since_date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
            # cls.cursor.execute("SELECT payload, dt FROM mqtt_outgoing where dt >= ?",(since_date,))

            cls.cursor.execute("SELECT payload, dt FROM mqtt_outgoing")
            result = cls.cursor.fetchall()
            return result
        else:
            return []
        
    @classmethod
    def select_count(cls)-> int:
        if cls.ready:

            cls.cursor.execute("SELECT count(*) FROM mqtt_outgoing")
            result = cls.cursor.fetchone()

            if isinstance(result,tuple):
                return result[0]
            return 0

    @classmethod
    def clear_data(cls):
        if cls.ready:
            cls.cursor.execute("Delete FROM mqtt_outgoing")
            cls.conn.commit()


    @classmethod
    def store(cls,payload:str,datetime_iso:str):
        if cls.ready:
            if cls.select_count() < cls.max_rows():
                cls.cursor.execute(
                    """
                INSERT INTO mqtt_outgoing (
                    payload, dt
                ) VALUES (?, ?)
                """,
                (
                    payload,
                    datetime_iso,
                ),
                )
                cls.conn.commit()
            else :
                print("Max row count reached , wont persist the data.")
    
    @classmethod
    def add_config(cls,payload):
        if cls.ready:
            cls.config_rows.append(payload)

    @classmethod
    def append(cls,payload:str,datetime_iso:str):
        if cls.ready:
            cls.rows.append((payload,datetime_iso))


"""
[
    {
        "light_event": [
            2,
            2,
            1
        ],
        "detail": {
            "port1": {
                "type": "SolidOff",
                "code": 2
            },
            "port2": {
                "type": "SolidOff",
                "code": 2
            },
            "port3": {
                "type": "SolidOn",
                "code": 1
            }
        },
        "data": [
            "22222222222222222222",
            "22222222222222222222",
            "11111111111111111111"
        ],
        "update_type": "Passive",
        "mac_client_id": "1",
        "client_id": null,
        "FREQUENCY": 0.1,
        "LIMIT_FREQUENCY": 20,
        "tower_type": null,
        "range": {
            "FAST_FLASH": [
                0.08,
                0.12
            ],
            "SLOW_FLASH": [
                0.4,
                0.8
            ],
            "SOLID_ON": [
                0.9,
                2.1
            ],
            "SOLID_OFF": [
                0.9,
                2.1
            ],
            "FLASH_ON_ONCE": [
                0.3,
                0.6
            ],
            "FLASH_OFF_ONCE": [
                0.3,
                0.6
            ]
        },
        "dt": "2024-01-17T12:36:36.224347"
    }
]

"""