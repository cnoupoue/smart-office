import mqtt
import LA66
import serial
import time

if __name__ == "__main__":
    mqtt.connect("broker.hivemq.com", 1883)
    port='/dev/ttyUSB0'
    baudrate=9600
    print("waiting for esp32 oled messages")
    try:
        with serial.Serial(port, baudrate, timeout=1) as ser:
            while True:
                if ser.in_waiting <= 0:
                    continue
                message = LA66.readMessage(ser)
                if message != None:
                    print("message received: " + message)
                    mqtt.publish("hepl/smartoffice/esp32",  "DOOR_ON")
                    time.sleep(2)
                    mqtt.publish("hepl/smartoffice/esp32",  "DOOR_OFF")
    except Exception as e:
        print("Error: " + e)