#!/bin/bash

# Définir le répertoire des certificats
CERT_DIR="../../certificates"

# Créer le répertoire s'il n'existe pas
mkdir -p "$CERT_DIR"

# Générer une clé privée
openssl genrsa -out "$CERT_DIR/mqtt.key" 2048
if [ $? -ne 0 ]; then
    echo "Erreur lors de la génération de la clé privée."
    exit 1
fi

# Générer une CSR (Certificate Signing Request)
openssl req -out "$CERT_DIR/mqtt.csr" -key "$CERT_DIR/mqtt.key" -new
if [ $? -ne 0 ]; then
    echo "Erreur lors de la génération de la CSR."
    exit 1
fi

# Copier le contenu du CSR dans le presse-papiers
if command -v xclip >/dev/null 2>&1; then
    xclip -selection clipboard < "$CERT_DIR/mqtt.csr"
    echo "Le contenu du CSR a été copié dans le presse-papiers."
elif command -v pbcopy >/dev/null 2>&1; then
    pbcopy < "$CERT_DIR/mqtt.csr"
    echo "Le contenu du CSR a été copié dans le presse-papiers."
else
    echo "Aucun utilitaire pour copier dans le presse-papiers n'a été trouvé. Veuillez copier manuellement le contenu du fichier CSR ci-dessous :"
    cat "$CERT_DIR/mqtt.csr"
fi

# Inviter l'utilisateur à utiliser le CSR
echo "Veuillez aller copier le contenu du CSR à l'adresse suivante : https://test.mosquitto.org/ssl/"
echo "Le CSR est disponible dans le fichier : $CERT_DIR/mqtt.csr"

