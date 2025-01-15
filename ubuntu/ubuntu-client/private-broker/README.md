# Smart Office MQTT Communication

This project uses a private MQTT broker to facilitate communication between a Raspberry Pi (RPI) and a server, with a UI for interaction. Below are the MQTT topics used for this communication.

## Installation

```bash
./install.sh
```

## Launch

```bash
./start.sh
```

## Topics Sent by the Raspberry Pi

- **Hello Request**  
  Topic: `smartoffice/1/<serial-id>/hello`  
  Description: Sends a hello request to the server.

- **Send Temperature**  
  Topic: `smartoffice/1/<serial-id>/temperature`  
  Data Type: `int`  
  Description: Sends the current temperature.

- **Send Light Sensor Data**  
  Topic: `smartoffice/1/<serial-id>/light_sensor`  
  Data Type: `int`  
  Description: Sends light intensity data.

- **Send Sound Sensor Data**  
  Topic: `smartoffice/1/<serial-id>/sound_sensor`  
  Data Type: `int`  
  Description: Sends sound level data.

- **Send GPS Data**  
  Topic: `smartoffice/1/<serial-id>/gps`  
  Data Type: `data`  
  Description: Sends GPS coordinates.

- **Send RFID Data**  
  Topic: `smartoffice/1/<serial-id>/rfid`  
  Data Type: `data`  
  Description: Sends RFID information.

## Topics Received by the Raspberry Pi

- **Update Local Data**  
  Topic: `smartoffice/1/<serial-id>/youare`  
  Example Value: `290C`  
  Description: Updates the local data on the RPI.

- **Control LED on ESP32**  
  Topic: `smartoffice/1/<serial-id>/led`  
  Example Value: `ON/OFF`  
  Description: Toggles the LED on or off.

- **Display Error on LCD + Activate Buzzer**  
  Topic: `smartoffice/1/<serial-id>/lcd`  
  Example Value: `ERROR: Temperature is high: 39°C`  
  Description: Displays a message on the LCD and activates the buzzer.

- **Control Camera**  
  Topic: `smartoffice/1/<serial-id>/camera`  
  Example Value: `ON/OFF`  
  Description: Turns the camera on or off.

## Overview

- The Raspberry Pi communicates with the private MQTT broker to send sensor data and receive commands from the server.
- The server processes the data and updates the UI based on the information provided by the Raspberry Pi.
- This system is designed for efficient communication and real-time updates in a smart office environment.
