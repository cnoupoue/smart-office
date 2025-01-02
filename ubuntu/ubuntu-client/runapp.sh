#!/bin/bash

sudo docker build -t mongo-iot-image:1.0 mongodb/

echo "MongoDB image rebuilt"

sudo docker compose -f docker-compose.yaml down

sudo docker compose -f docker-compose.yaml up -d

echo "MongoDB up"

echo "Stop Flask and Node Red"
node-red stop
pkill -f flask
kill -9 $(lsof -t -i :1880)
kill -9 $(lsof -t -i :5050)
sleep 1

echo "Lauching Flask API"
python3 flask-nginx/auth_server_api.py &
sleep 1

echo "Launching Node Red"
node-red &
