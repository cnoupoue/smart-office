#!/bin/bash

sudo openssl genrsa -des3 -out ../../../certificates/nodered.key 2048

sudo openssl req -new -out ../../../certificates/nodered.csr -key ../../../certificates/nodered.key

sudo openssl x509 -req -in ../../../certificates/nodered.csr -CA ../../../certificates/ca.crt -CAkey ../../../certificates/ca.key -CAcreateserial -out ../../../certificates/nodered.crt -days 365

sudo openssl x509 -in ../../../certificates/nodered.crt -out ../../../certificates/noderedcert.pem -outform PEM

sudo openssl rsa -in ../../../certificates/nodered.key -out ../../../certificates/noderedkey.pem -outform PEM

sudo cp ../../../certificates/noderedkey.pem ~/.node-red

sudo cp ../../../certificates/noderedcert.pem ~/.node-red
