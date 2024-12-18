# MongoDB

We use MongoDB as our NoSQL database to store the client, the rooms, the reserved rooms, and the logs

## Scheme

The database schema is available in this repository : `database.png`

## Mongo Instance

We used Docker to containerize our database. 

The Dockerfile is available in this folder.

The credits for the database are : `hepl` and password is `heplhepl`

## Launch the database

`sudo docker compose -f docker-compose.yaml up -d`

`sudo docker exec -it mongo-client mongosh`

