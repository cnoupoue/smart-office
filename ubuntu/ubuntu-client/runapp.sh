#!/bin/bash

check_avahi() {
    if ! dpkg -l | grep -qw avahi-daemon; then
        echo "avahi-daemon not found. Installing..."
        sudo apt update
        sudo apt install -y avahi-daemon && echo "avahi-daemon installed successfully."
        sudo systemctl enable avahi-daemon && echo "avahi-daemon enabled."
    fi
}

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

check_avahi
sudo hostnamectl set-hostname smartoffice-company1
sudo systemctl restart avahi-daemon

# Demander à l'utilisateur s'il souhaite reconstruire l'image MongoDB
read -p "Do you want to rebuild the MongoDB Docker image? (y/n): " rebuild_choice
if [[ "$rebuild_choice" =~ ^[Yy]$ ]]; then
    echo "Rebuilding MongoDB image..."
    sudo docker build -t mongo-iot-image:1.0 mongodb/ && echo "MongoDB image rebuilt"
    echo "Restarting Docker Compose services..."
    sudo docker compose -f docker-compose.yaml down
    sudo docker compose -f docker-compose.yaml up -d && echo "Docker Compose services are up"
else
    echo "Skipping MongoDB image rebuild."
fi

# Arrêter les processus existants
stop_processes

# Délai avant de relancer les processus
sleep 2

# Relancer Flask et Node-RED
start_processes

# Lancer Nginx via le script nginx/start_nginx.sh
#echo "Starting Nginx using nginx/start_nginx.sh..."
#cd nginx
#bash ./start_nginx.sh && echo "Nginx started successfully" || echo "Failed to start Nginx"
#cd "$(dirname "$0")"
#echo "All services have been restarted successfully."

