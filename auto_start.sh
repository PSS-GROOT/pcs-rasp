#!/bin/bash

echo "Script started at $(date)" >> /home/pi/Desktop/script_log.txt

sleep 5

cd /home/pi/Desktop/pcs-rasp
bash raspStart.sh &

cd /home/pi/Desktop/PCS/
./PCS

echo "Script completed at $(date)" >> /home/pi/Desktop/script_log.txt

## usage
# crontab -e
# @reboot /bin/bash /home/pi/Desktop/auto_start.sh