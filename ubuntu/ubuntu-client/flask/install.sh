#!/bin/sh

echo "Installation de flask"
pip install --break-system-packages flask flask-cors flask-jwt-extended flask-wtf flask-pymongo bcrypt pyjwt flask-session

sudo openssl genrsa -out ../../../certificates/flask.key 2048
sudo openssl req -new -key ../../../certificates/flask.key -out ../../../certificates/flask.csr
sudo openssl x509 -req -in ../../../certificates/flask.csr -CA ../../../certificates/ca.crt -CAkey ../../../certificates/ca.key -CAcreateserial -out ../../../certificates/flask.crt -days 365

