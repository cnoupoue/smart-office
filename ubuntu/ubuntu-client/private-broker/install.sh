#!/bin/bash

echo "Mise à jour des paquets..."
sudo apt update -y

echo "Installation de Mosquitto..."
sudo apt install -y mosquitto

echo "Installation de Mosquitto Clients..."
sudo apt install -y mosquitto-clients

cp mosquitto.conf /etc/mosquitto/mosquitto.conf
echo "Arrêt des processus Mosquitto..."
sudo killall mosquitto

echo "Démarrage de Mosquitto en mode verbeux..."
sudo mosquitto -v

