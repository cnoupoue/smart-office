#!/bin/bash

sudo killall mosquitto

echo "Démarrage de Mosquitto en mode verbeux..."
gnome-terminal -- bash -c "sudo mosquitto -c /etc/mosquitto/mosquitto.conf -v; exec bash"
