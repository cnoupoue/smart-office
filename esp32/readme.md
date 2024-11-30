# Étapes de configuration du ESP32 pour exécuter le code
1. Bien brancher les capteurs au ESP
1. Connecter ESP32 au PC avec un bon câble
1. Vérifier qu'il est connecté à la VM UBunru
1. Identifier le fichier `main.py` à envoyer sur ESP32
1. Lancer la commande `ampy --port /dev/ttyUSB0 put main.py`
    - si la commande ne répond pas, débrancher et rebrancher ESP32 en vérifiant s'il est connecté au Ubuntu.
1. connecter au minicom `sudo minicom`.
1. cliquer sur le bouton `reset` du ESP32 pour voir apparaitre les prints dans le minicom.

## S'il faut mettre à jour le fichier `main.py`:
- !!! Fermer le terminal minicom
- Lancer la commande `ampy --port /dev/ttyUSB0 put main.py`
- !!! Fermer le terminal minicom

## S'il faut exécuter un autre code sans écraser le fichier `main.py`, et sans passer par `minicom`, on peut uploader un fichier différent et l'exécuter directement:
1. Lancer la commande `ampy --port /dev/ttyUSB0 put led.py`  pour upload un fichier
2. Lancer la commande `ampy --port /dev/ttyUSB0 run led.py` pour exécuter ce fichier sur ESP32
   - Les prints devront apparaitre après cette commande sans passer par minicom.

### Pour le code actuelle, le redémarrage dure 15-20 secondes avant l'envoie de la première valeur de température.