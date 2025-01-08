# Node RED

A three-part website for the client hosted on the client VM using NodeRed.

## Files

* `flows.json` is the data for node-red flow
* `settings.json` is the node-red configuration
* `package.json` are the installed packages

To copy them from the `.node-red` package, please use the `./get_nodered_config.sh` script

Here's the list of packages we installed 
- node-red-dashboard
- node-red-contrib-mongodb4
- node-red-contrib-uimedia
- node-red-node-ui-table
- node-red-contrib-web-worldmap

## Parts

* A dashboard with RPI data
* A reservation pannel with the used rooms (a calendar to display free rooms, via a mongodb 
* A log part for the admin with all MQTT requests etc
* A support to help the client to contact us (with webex)

## What we did 

* Install Node Red (the user is `hepl` and password `heplhepl`
* Launch node red `node-red &` then go to the [localhost](localhost:1880)

## What we have to do

Secure Node Red with https
-> generate a CA for the whole project
-> edit `.node-red/settings.json`
-> set node-red starts at the boot

Using of httpNodeCors to allow external origins for HTTP request (cfr. nginx)
