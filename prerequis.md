# En général
- Chaque étudiant devra connaître tout le projet
- 

# Ce que j'ai appris
Nous avons grandement apprécié votre soutient tout au long du projet, vous avez apporté des idées innovantes auxquelles nous n'avions pas pensées comme le système de réserve de locaux, Nous n'avions pas pensé à aller au delà car nous pensions que le projet tournait autour des capteurs. 
Personnellement, j'ai pris plaisir à réaliser ce projet, même si parfois, je perdait énormément à résoudre les problèmes qui arrivaient l'une après l'autre.

# Prérequis
✅ Un raspberry pi avec carte GrovePi et adaptateur LA66-LoRaWan  
✅ Un ESP32 qui communiquera en WiFi et en MQTT (utilisation de Micropython)  
❌ Ubuntu Client avec utilisation d’au moins un container docker  
❌ Ubuntu Serveur avec utilisation d’au moins un container docker  
❌ Un broker public du type test.mosquitto.org avec utilisation de certificats (test.mosquitto.org/ssl) port 8884 ainsi 
❌ un broker privé qui tournera sur une des VM Ubuntu 22.04  
❌ Votre smartphone pour vous connecter à une interface Web (dashboards Node-Red)  
❌ Votre smartphone pour vous connecter à une room web.webex.com  
✅ Une carte Heltec-esp32s3-oled-LoRa  
✅ L’afficheur LCD connecté au GrovePi  
✅ La connexion au réseau WiFi sera sécurisée en WPA2-PSK (connection via 4G ou WiFi IOT).   
❌ accès à l’interface graphique du RPi en VNC à partir d’une VM Ubuntu 22.04.  
✅ L’ESP32 fera au minimum l’acquisition de 2 mesures à l’aide de capteurs et transmettra les résultats en MQTT via le réseau WiFi.  
❌ Nodered  
✅ Paho  
✅ Python multithreading  
✅ MongoDB  
✅ Utiliser un API rest non vue au cours (qualité air)  
❌ L’accès à ce API s’effectuera avec la librairie Python “requests”  
❌ Au moins une requête à l’API shodan.  
❌📍 vous écrirez votre propre API REST avec authentification (Flask)  
✅ Au moins 5 capteurs parmi:  
- distance
- luminosité ✅
- capteur angulaire
- capteur de son ✅
- température ✅
- bouton  ✅
- GPS. ✅
✅ Au moins 2 parmi:
- Buzzer ✅
- LED ✅
- Relais ✅
🕖 Au moins 2 types d'accès
❌ Notifications des événements par mail
❌ Notifications des événements par SMS
❌ Loggins sauvegardées dans la database sur un UBUNTU (avec timestamp)
🕖 Afficher l'historique des mesures
🕖 Filtre historique des mesures avec un champs date
✅ Utiliser RFID
❌ Utiliser NFC
❌ Utiliser la camera
✅ Utiliser LoRa entre Heltec et LA66
✅ Heltec sera émetteur et LA66 récepteur
✅ Messages pertinentes à afficher sur Heltec OLED
✅ Au moins une mesure sur Heltec
❌ Sécuriser au moins une fois MQTT avec certificat coté client et serveur
❌ QoS 2 sans TLS au moins une fois
🕖📍 Une fois afficher carte dashboard (noeud Worldmap)
✅ Le RPI, ESP32, Heltec démarrent automatiquement