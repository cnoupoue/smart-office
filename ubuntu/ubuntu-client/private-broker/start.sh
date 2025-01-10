#!/bin/bash

sudo killall mosquitto

echo "Démarrage de Mosquitto en mode verbeux..."
gnome-terminal -- bash -c "sudo mosquitto -v; exec bash"
