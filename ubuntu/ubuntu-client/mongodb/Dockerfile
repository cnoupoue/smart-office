FROM mongo:latest

LABEL maintainer="Cameron Noupoue"

COPY initdb.js /docker-entrypoint-initdb.d/initDB.js

RUN apt-get update && apt-get install -y iproute2 iputils-ping

EXPOSE 27017
