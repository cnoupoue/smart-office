import controllers.common as common
import utils.la66 as la66
import serial
import env
import controllers.mqtt_controller as mqtt_controller

def run():
    ser = None
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        while True:
            if ser.in_waiting <= 0:
                continue
            message = la66.read(ser)
            if not message or not message.startswith("smartoffice:"):
                continue
            extractedMessage = message.split(":")[1]
            mqtt_controller.put_in_publish_queue(env.RFID, extractedMessage)
                
    except Exception as e:
        print("Error: " + str(e))
    finally: ser.close()