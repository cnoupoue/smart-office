#!/bin/sh

echo "Installation de flask"
pip install --break-system-packages flask flask-cors flask-jwt-extended flask-wtf

echo "\nEspace disque disponible :"
df -h

echo "\nTop 5 des processus par utilisation mémoire :"
ps aux --sort=-%mem | head -n 6

