#!/bin/bash

sudo killall mosquitto

echo "Démarrage de Mosquitto en mode verbeux..."
sudo mosquitto -v

