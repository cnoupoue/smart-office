FROM mongo:latest


LABEL maintainer="Kotiyev Nasser"

COPY initdb.js /docker-entrypoint-initdb.d/initDB.js

RUN apt-get update && \
    apt-get install -y iproute2 iputils-ping && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 27017
