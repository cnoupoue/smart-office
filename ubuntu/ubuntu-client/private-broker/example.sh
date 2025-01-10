#!/bin/bash

gnome-terminal -- bash -c "mosquitto_sub -h localhost -t mytopic; exec bash"
gnome-terminal -- bash -c "mosquitto_pub -h localhost -t mytopic -m "hello"; exec bash"
