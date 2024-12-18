#!/bin/bash

sudo docker run --name mongo-client -e MONGO_INITDB_ROOT_USERNAME=hepl -e MONGO_INITDB_ROOT_PASSWORD=heplhepl -d mongo-iot-image:1.0
