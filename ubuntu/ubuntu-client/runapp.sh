#!/bin/bash

# Fonction pour couper les processus Flask et Node-RED
stop_processes() {
    echo "Stopping Node-RED and Flask..."
    pkill -f "node-red" && echo "Node-RED stopped" || echo "Node-RED not running"
    pkill -f flask && echo "Flask stopped" || echo "Flask not running"
    kill -9 $(lsof -t -i :5000 2>/dev/null) && echo "Port 5000 freed" || echo "Port 5000 not in use"
}

# Fonction pour relancer Flask et Node-RED dans des terminaux séparés
start_processes() {
    echo "Launching Flask API in a new terminal..."
    gnome-terminal -- bash -c "python3 flask/auth_server_api.py; exec bash" &

    echo "Launching Node-RED in a new terminal..."
    gnome-terminal -- bash -c "node-red; exec bash" &
}

# Demander à l'utilisateur s'il souhaite reconstruire l'image MongoDB
read -p "Do you want to rebuild the MongoDB Docker image? (y/n): " rebuild_choice
if [[ "$rebuild_choice" =~ ^[Yy]$ ]]; then
    echo "Rebuilding MongoDB image..."
    sudo docker build -t mongo-iot-image:1.0 mongodb/ && echo "MongoDB image rebuilt"
else
    echo "Skipping MongoDB image rebuild."
fi

# Arrêter et redémarrer les conteneurs Docker
echo "Restarting Docker Compose services..."
sudo docker compose -f docker-compose.yaml down
sudo docker compose -f docker-compose.yaml up -d && echo "Docker Compose services are up"

# Arrêter les processus existants
stop_processes

# Délai avant de relancer les processus
sleep 2

# Relancer Flask et Node-RED
start_processes

echo "All services have been restarted successfully."

