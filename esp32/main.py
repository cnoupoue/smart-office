import dht
import machine
import time
import network
from umqtt.simple import MQTTClient
import uasyncio as asyncio

PUB_DELAY = 5

SSID = "kotinas"         # Your Wi-Fi SSID
PASSWORD = "rootroot"    # Your Wi-Fi Password

BROKER = "test.mosquitto.org"  # Replace with your broker address
TOPIC_TEMP = "hepl/smartoffice/temperature"
TOPIC_SUB = "hepl/smartoffice/esp32"

LED = machine.Pin(5, machine.Pin.OUT)
RELAY = machine.Pin(18, machine.Pin.OUT)
TEMPERATURE = dht.DHT11(machine.Pin(19))

async def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Connecting to Wi-Fi...")
    while not wlan.isconnected():
        time.sleep(1)
    print("Connected to Wi-Fi:", wlan.ifconfig())

def connect_mqtt():
    client = MQTTClient("esp32", BROKER)
    client.connect()
    print("Connected to MQTT Broker")
    return client

def getTemperature():
    TEMPERATURE.measure()
    return str(TEMPERATURE.temperature())

def pub_mqtt(client, message):
    client.publish(TOPIC_TEMP, message)
    print(f"Published {message} for topic {TOPIC_TEMP}")

def sub_callback(topic, msg):
    m = msg.decode()
    if m == "RESERVED_ON":
        LED.on()
        print("reserved")
    elif m == "RESERVED_OFF":
        LED.off()
        print("not reserved")
    elif m == "DOOR_ON":
        RELAY.on()
        print("door open")
    elif m == "DOOR_OFF":
        RELAY.off()
        print("door close")
    else:
        print(f"unknown message: {m}")

async def sub_mqtt(client) :
    client.set_callback(sub_callback)
    client.connect()
    client.subscribe(TOPIC_SUB)
    print(f"Subscribed to {TOPIC_SUB}")

    try:
        while True:
            client.check_msg()  # Non-blocking check for messages
            await asyncio.sleep(1)  # Async sleep to yield control
    finally:
        print("Disconnecting...")
        client.disconnect()

async def pub_mqtt_temp(client) :
    try:
        while True:
            pub_mqtt(client, getTemperature())
            await asyncio.sleep(PUB_DELAY)
    finally:
        print("Disconnecting...")
        client.disconnect()

# code
async def main():
    await connect_wifi()
    # Run the MQTT subscriber
    client = MQTTClient("esp32", BROKER)
    # Async task for subscription
    asyncio.create_task(sub_mqtt(client))
    # Async task for publication
    asyncio.create_task(pub_mqtt_temp(client))
    # Infinite loop necessary to keep program alive, otherwise it will stop when reaching the end of the code
    while True:
        await asyncio.sleep(0.1)

asyncio.run(main())