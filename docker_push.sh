#!/bin/bash
docker tag pcs-rasp:latest pentapss.azurecr.io/pcs-rasp:latest

docker push pentapss.azurecr.io/pcs-rasp:latest