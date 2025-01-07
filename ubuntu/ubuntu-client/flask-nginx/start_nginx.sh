#!/bin/sh

sudo cp nginx.conf /etc/nginx/nginx.conf
sudo cp login.html /etc/nginx/html/login.html
sudo systemctl restart nginx

