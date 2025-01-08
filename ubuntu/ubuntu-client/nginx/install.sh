#!/bin/sh
sudo apt update

sudo apt install -y nginx

sudo cp nginx.conf /etc/nginx/nginx.conf
sudo cp login.html /etc/nginx/html/login.html

sudo systemctl enable nginx

