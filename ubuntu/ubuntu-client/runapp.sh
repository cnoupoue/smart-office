#!/bin/bash

sudo docker build -t mongo-iot-image:1.0 mongodb/Dockefile

sudo docker build -t nodered-iot-image:1.0 node-red/Dockerfile

echo "Images rebuilt"

sudo docker compose -f docker-compose.yaml down

sudo docker compose -f docker-compose.yaml up -d
