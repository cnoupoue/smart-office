#!/bin/bash

DIR_NAME="certificates"

mkdir -p "$DIR_NAME"
cd "$DIR_NAME" || exit

echo "Updating packages..."

if ! command -v openssl &> /dev/null; then
    echo "OpenSSL is not installed. Installing..."
    sudo apt update
    sudo apt install -y openssl
else
    echo "OpenSSL is already installed."
fi

echo "Copying openssl_example.cnf to /etc/ssl/openssl.cnf..."
sudo cp openssl_example.cnf /etc/ssl/openssl.cnf

echo "Generating private key ca.key..."
sudo openssl genrsa -out ca.key 2048

echo "Generating self-signed certificate ca.crt..."
sudo openssl req -new -x509 -days 365 -key ca.key -out ca.crt

echo "Certificate details for ca.crt:"
openssl x509 -in ca.crt -text -noout

