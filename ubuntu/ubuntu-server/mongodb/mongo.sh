    echo "Rebuilding MongoDB image..."
    sudo docker build -t mongo-iot-image:1.0 ./ && echo "MongoDB image rebuilt"
    echo "Restarting Docker Compose services..."
    sudo docker compose -f docker-compose.yaml down
    sudo docker compose -f docker-compose.yaml up -d && echo "Docker Compose services are up"