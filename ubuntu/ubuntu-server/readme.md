# pour autoriser remote desktop sur ubuntu oracle

voir : https://www.youtube.com/watch?v=C0nxOZBo6Dw
# pour installer un GUI sur ubuntu server 
https://www.youtube.com/watch?v=ODhGNe0s4lI

# Pour mettre en place VNC sur ubuntu et RPI
## sur ubuntu
### ouvrir les ports
```
sudo iptables -F && sudo iptables -X && sudo iptables -t nat -F && sudo iptables -t nat -X && sudo iptables -t mangle -F && sudo iptables -t mangle -X && sudo iptables -t raw -F && sudo iptables -t raw -X && sudo iptables -P INPUT ACCEPT && sudo iptables -P FORWARD ACCEPT && sudo iptables -P OUTPUT ACCEPT
sudo iptables -A INPUT -p tcp --dport 5901 -j ACCEPT
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
### se connecter en GUI
lancer l'application xtightvncviewer avec la commande `xtightvncviewer`, ensuite entrer le port utilisé dans le reverse tunneling `localhost:5909`, et se connecter avec le mot de passe `smartoffice`

# Lancer application python
Dans `/home/pi/Documents/officestation/main.py`
```bash
nohup python3 main.py &
```
# Donner un access ssl à la RPI
```bash
ngrok tcp 22
```