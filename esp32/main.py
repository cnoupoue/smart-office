import dht
import machine
import time
import network
from umqtt.simple import MQTTClient
import uasyncio as asyncio
import json

PUB_DELAY = 2

SSID = "kotinas"         # Your Wi-Fi SSID
PASSWORD = "rootroot"    # Your Wi-Fi Password
COMPANY_ID = "1"
RPI_SERIAL_ID = "1000000044888d31"
BROKER = "broker.hivemq.com"  # Replace with your broker address
TOPIC_TEMP = f"smartoffice/{COMPANY_ID}/{RPI_SERIAL_ID}/temperature"
TOPIC_SUB_RELAY = f"smartoffice/{COMPANY_ID}/{RPI_SERIAL_ID}/relay"
TOPIC_SUB_LED = f"smartoffice/{COMPANY_ID}/{RPI_SERIAL_ID}/led"

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

def connect_mqtt(client_id):
    client = MQTTClient(client_id, BROKER)
    client.connect()
    print(f"Connected to MQTT Broker with ID: {client_id}")
    return client

def getTemperature():
    TEMPERATURE.measure()
    data = {"temperature": str(TEMPERATURE.temperature()), "humidity": str(TEMPERATURE.humidity()),}
    return json.dumps(data)

def pub_mqtt(client, message):
    client.publish(TOPIC_TEMP, message)
    print(f"Published {message} for topic {TOPIC_TEMP}")

def sub_callback(topic, msg):
    
    m : str= msg.decode()
    t : str= topic.decode()
    if t == TOPIC_SUB_LED:
        if m == "ON":
            LED.off()
            time.sleep(0.1)
            LED.on()
            print("reserved")
        elif m == "OFF":
            LED.on()
            time.sleep(0.1)
            LED.off()
            print("not reserved")
        else:
            print(f"unknown message: {m}")
    elif t == TOPIC_SUB_RELAY:
        if m == "ON":
            RELAY.on()
            print("door open")
        elif m == "OFF":
            RELAY.off()
            print("door close")
        elif m.startswith("ON_OFF:"):
            delay = int(m.split(":")[1])
            RELAY.on()
            time.sleep(delay)
            RELAY.off()
            print("door close")
        else:
            print(f"unknown message: {m}")
    else:
        print(f"unknown topic: {t}")


async def sub_mqtt():
    client = connect_mqtt("esp32_sub")
    client.set_callback(sub_callback)
    while True:
        try:
            client.connect()
            client.subscribe(TOPIC_SUB_LED)
            client.subscribe(TOPIC_SUB_RELAY)
            print(f"Subscribed to {TOPIC_SUB_LED} and {TOPIC_SUB_RELAY}")

            while True:
                client.check_msg()  # Non-blocking check for messages
                await asyncio.sleep(1)
        except OSError as e:
            print(f"Error in sub_mqtt: {e}, reconnecting...")
            await asyncio.sleep(5)  # Wait before retrying

async def pub_mqtt_temp():
    client = connect_mqtt("esp32_pub")
    try:
        while True:
            temp = getTemperature()
            pub_mqtt(client, temp)
            await asyncio.sleep(PUB_DELAY)
    except Exception as e:
        print(f"Error in pub_mqtt_temp: {e}")
    finally:
        print("Disconnecting publisher...")
        client.disconnect()

# code
async def main():
    try:
        await connect_wifi()
        # Create separate tasks for subscription and publication
        asyncio.create_task(pub_mqtt_temp())
        asyncio.create_task(sub_mqtt())

        # indicator of ready
        await asyncio.sleep(0.5)

        # Infinite loop necessary to keep program alive, otherwise it will stop when reaching the end of the code
        while True:
            await asyncio.sleep(0.5)
    except Exception as e:
        print(f"Error in pub_mqtt_temp: {e}")

asyncio.run(main())