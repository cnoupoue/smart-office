#!/bin/bash

sudo docker build -t mongo-iot-image:1.0 mongodb/

echo "MongoDB image rebuilt"

sudo docker compose -f docker-compose.yaml down

sudo docker compose -f docker-compose.yaml up -d
