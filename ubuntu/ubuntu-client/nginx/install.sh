#!/bin/sh
sudo apt update

sudo apt install -y nginx

sudo cp nginx.conf /etc/nginx/nginx.conf
sudo cp login.html /etc/nginx/html/login.html

sudo openssl genrsa -out ../../../certificates/nginx.key 2048
sudo openssl req -new -key ../../../certificates/nginx.key -out ../../../certificates/nginx.csr
sudo openssl x509 -req -in ../../../certificates/nginx.csr -CA ../../../certificates/ca.crt -CAkey ../../../certificates/ca.key -CAcreateserial -out ../../../certificates/nginx.crt -days 365

sudo mkdir -p /etc/nginx/ssl
sudo cp ../../../certificates/nginx.* /etc/nginx/ssl

sudo systemctl enable nginx

