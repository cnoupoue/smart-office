# Pour pouvoir faire fonctionner le GPS
Source: https://www.youtube.com/watch?v=N8fH0nc9v9Q

## Modifier ce fichier
```bash
sudo nano /boot/config.txt
    dtparam=spi=on
    dtoverlay=pi3-disable-bt
    core_freq=250
    enable_uart=1
    force_turbo=1
```
## Modifier ce fichier
```bash
sudo cp /boot/cmdline.txt /boot/cmdline_backup.txt
sudo nano /boot/cmdline.txt
```
```
dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles
```
```bash
sudo reboot
```
## Pour afficher les valeurs de retour
```bash
sudo cat /dev/ttyAMA0
```
# Pour pouvoir exécuter le programme python avec les imports fonctionnels
Lancer controllerLA66.py
```
python3 controllerLA66.py
```

Pour que le code python fonctionne, ajouter ça dans le fichier, ce chemin correspond au chemin racine du projet python :
```bash
nano ~/.bashrc
    export PYTHONPATH="~/Documents/office-station:$PYTHONPATH"
source ~/.bashrc
```

# Mise en place mot de passe vnc
```bash
sudo vncpasswd -weakpwd -service
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
ssh -i ./ubuntu_oracle.key -R 5910:localhost:5901 ubuntu@darkquarx.be
```
Attention, il faut s'assurer que sur Ubuntu server, le processus n'utilise pas le port 5910, il faut tuer ce processus avec la commande:
```bash
sudo kill $(sudo lsof -t -i:5910)
ss -aptn | grep 5910
```
# pour que l'écran RPI s'affiche sur VNC:
```bash
sudo nano /boot/config.txt
```
```bash
hdmi_force_hotplug=1
hdmi_group=2
hdmi_mode=9
```

# Mise en place de la camera:
https://www.youtube.com/watch?v=yhM1NhD-kGs

# mise en place streaming camera
suivre le tuto : 
https://randomnerdtutorials.com/video-streaming-with-raspberry-pi-camera/

Ne pas oublier de modifier le code python en ajoutant cette ligne dans `finally` à la fin
```python
camera.close()
```

# lancer les scripts au démarrage:
```bash
crontab -e
```

```bash
@reboot /home/pi/Documents/office-station/script.sh

```