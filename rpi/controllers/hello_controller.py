import controllers.common as common
import env
import time
import controllers.mqtt_controller as mqtt_controller

def run():
    while True:
        time.sleep(env.HELLO_DELAY)
        mqtt_controller.ask_for_premise()