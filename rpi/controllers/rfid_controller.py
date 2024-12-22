import controllers.common
import utils.mqtt as mqtt
import utils.la66 as la66
import serial
import time

def start():
    mqtt.connect("broker.hivemq.com", 1883)
    print("waiting for esp32 oled messages")
    ser = None
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        while True:
            if ser.in_waiting <= 0:
                continue
            message = la66.readMessage(ser)
            if message != None:
                print("message received: " + message)
                mqtt.publish("hepl/smartoffice/esp32",  "DOOR_ON")
                time.sleep(2)
                mqtt.publish("hepl/smartoffice/esp32",  "DOOR_OFF")
                
    except Exception as e:
        print("Error: " + e)
    finally: ser.close()