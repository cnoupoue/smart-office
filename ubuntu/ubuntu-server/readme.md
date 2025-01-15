# pour autoriser remote desktop sur ubuntu oracle

voir : https://www.youtube.com/watch?v=C0nxOZBo6Dw
# pour installer un GUI sur ubuntu server 
https://www.youtube.com/watch?v=ODhGNe0s4lI

# Pour mettre en place VNC sur ubuntu et RPI
## sur ubuntu
### ouvrir les ports
```
sudo iptables -F
# Allow access to Docker containers
sudo iptables -A INPUT -i docker0 -j ACCEPT
sudo iptables -A FORWARD -i docker0 -o docker0 -j ACCEPT
sudo iptables -A FORWARD -i docker0 -o eth0 -j ACCEPT
sudo iptables -A FORWARD -i eth0 -o docker0 -j ACCEPT
# Allow loopback (localhost) traffic
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A OUTPUT -o lo -j ACCEPT
# Allow Docker container communication with the host
sudo iptables -A DOCKER -d 172.18.0.2 -p tcp --dport 27017 -j ACCEPT
# Accept incoming connections for other necessary services
sudo iptables -A INPUT -p tcp --dport 5901 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 5000 -j ACCEPT
```
### lancer une instance VNC
```
user@mc-server$ sudo vncserver -localhost no
```

## sur RPI
### installer un serveur vnc
```
sudo apt update
sudo apt install tightvncserver
vncserver :1
```

Créer un SSH reversed tunneling
```
ssh -i ./ubuntu_oracle.key -R 5909:localhost:5901 ubuntu@darkquarx.be 
```
## sur ubuntu
## se connecter à Ubuntu via windows:
lancer tightVNC viewer, mettre l'adresse `darkquarx.be:5901` avec le mot de passe `smartoffice`
### se connecter en GUI à partir de ubuntu
lancer l'application xtightvncviewer avec la commande `xtightvncviewer`, ensuite entrer le port utilisé dans le reverse tunneling `localhost:5910`, et se connecter avec le mot de passe `smartoffice`
```bash
xtightvncviewer localhost:5910

# si ne fonctionne pas, check tunnel ssh, il se peux que lorsque l'on déconnecte le RPI, le serveur garde la connexion tunnel ssh sur le port 5910 qui empêche une nouvelle tunnelle de se créer
sudo lsof -i :5910
sudo netstat -tuln | grep 5910
kill <pid>
```

# Lancer application python
Dans `/home/pi/Documents/officestation/main.py`
```bash
nohup python3 main.py &
```
# Donner un access ssl à la RPI
```bash
ngrok tcp 22
```

# TLS mosquitto.org
openssl genrsa -out client.key
openssl -new -key client.key -out client.csr -subj "/C=BE/ST=Liege/L=Liege/O=DeskSphere/OU=OrgUnit/CN=NasCam"
openssl x509 -in client.crt -out clientcrt.pem -outform PEM
openssl rsa -in client.key -out clientkey.pem -outform PEM

# Pour flask sécurisé https:
openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout server.key -out server.crt -subj "/C=BE/ST=Liege/L=Liege/O=DeskSphere/OU=OrgUnit/CN=NasCam"

# pour accéder en ssh:
ssh -i C:\Users\neutr\.ssh\ubuntu_oracle.key -o "ServerAliveInterval 60" ubuntu@89.168.47.217