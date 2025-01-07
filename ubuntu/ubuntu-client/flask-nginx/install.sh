#!/bin/sh

echo "Installation de flask"
pip install --break-system-packages flask flask-cors flask-jwt-extended flask-wtf flask-pymongo bcrypt pyjwt flask-session

sudo apt install -y nginx
sudo systemctl enable nginx
sudo systemctl status nginx

sudo cp nginx.conf /etc/nginx/nginx.conf
sudo cp login.html /etc/nginx/html/login.html
