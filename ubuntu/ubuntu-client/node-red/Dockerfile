FROM nodered/node-red:latest

COPY settings.js /data/settings.js
COPY package.json /data/package.json
COPY flows.json /data/flows.json

EXPOSE 1880

CMD ["npm", "start", "--", "--userDir", "/data"]

