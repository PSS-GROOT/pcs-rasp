#!/bin/bash
docker login -u deploy-token -p dJZ9XiewfZOXDfiR/voWWKD7ObKutV5R4F4/ZJTwZo+ACRCEoAxl pentapss.azurecr.io

docker tag pcs-rasp:latest pentapss.azurecr.io/pcs-rasp:latest

docker push pentapss.azurecr.io/pcs-rasp:latest