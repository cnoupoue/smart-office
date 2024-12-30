import os
import controllers.common as common
import env
from utils.mqtt import MQTT
import controllers.lcd_controller as lcd_controller
import controllers.buzzer_controller as buzzer_controller
import time
import queue

MQTTC : MQTT = None
message_queue = queue.Queue()
INIT_STATUS = True

def init():
    lcd_controller.display_info("Demarrage de \nl'appareil...")
    global MQTTC
    MQTTC = MQTT(sub_callback = manage_subscribed_topics)
    MQTTC.connect(url=env.BROKER, port=env.PORT)
    MQTTC.subscribe(env.HELLO_TOPIC, 2)
    MQTTC.subscribe(env.YOU_ARE_TOPIC)

# ask to server the premise
def ask_for_premise():
    MQTTC.publish(env.HELLO_TOPIC, "Hello", 2)

# define different actions depending on the received message
def manage_subscribed_topics(topic: str, value: str) -> None:
    global INIT_STATUS
    print(topic + " : " + value)
    if topic == env.YOU_ARE_TOPIC:
        # Why is there "None" and None for common.get_premise() ?
        # Because it's to display "Searching Server" and "Found server" once with None
        # Once these messages displayed, they won't be displayed because the previous premise 
        #   will have "None"
        old_premise = common.get_premise()
        if value == "NULL":
            # simulates no-response from the server
            return
        elif value == "NONE":
            if old_premise == None and INIT_STATUS:
                INIT_STATUS= False
                lcd_controller.display_success("Serveur trouve")
                time.sleep(2)
            common.set_premise("NONE")
            lcd_controller.display_warning("sans local, id=\n" + env.SERIAL_ID)
            time.sleep(0.5)
            return
        elif old_premise not in (value, "NULL", None):
            common.set_premise(value)
            lcd_controller.display_success(f"Local modifie: \n{old_premise} -> {value}")
            time.sleep(2)
            lcd_controller.display_info("Mon local est: \n" + value)
        else:
            if old_premise is None and INIT_STATUS:
                INIT_STATUS= False
                lcd_controller.display_success("Serveur trouve")
                time.sleep(2)
            lcd_controller.display_info("Mon local est: \n" + value)
            time.sleep(0.5)
        common.set_premise(value)
    # subscribed to my own to ensure that mqtt is started and then display the message, (haven't found other solutions)
    elif topic == env.HELLO_TOPIC:
        if (common.get_premise() is None and INIT_STATUS):
            lcd_controller.display_warning("Recherche serveur en cours...")
    elif common.get_premise() == None:
        # if local is not defined, it means that, raspberry hasn't contacted the server yet
        return
    elif topic == common.get_topic(env.RFID):
        buzzer_controller.three_quick_bip()
        publish(env.RELAY, "ON_OFF:5")
    elif topic == common.get_topic(env.BUZZER):
        if value == "ON":
            buzzer_controller.start()
        if value == "OFF":
            buzzer_controller.stop()
    elif topic == common.get_topic(env.LCD):
        type,message = value.split(";")
        if type == "ERROR":
            buzzer_controller.start()
            lcd_controller.display_error(message)
    elif topic == common.get_topic(env.BUTTON):
        lcd_controller.display_info("Mon local est: \n" + common.get_premise())
        buzzer_controller.stop()
    else:
        print("Unknown topic")

# put publication data in a Queue, to publish in order
def publish(topic: str, payload, qos=2):
    # if topic starts with "smartoffice/", it's a full topic path.
    # but if it starts with something else, it's a relative topic path
    if topic.startswith(env.MQTT_ROOT_TOPIC):
        message_queue.put((topic, payload, qos))
    else:
        message_queue.put((common.get_topic(topic), payload, qos))

def subscribeToOtherTopics():
    MQTTC.subscribe(common.get_topic(env.BUZZER))
    MQTTC.subscribe(common.get_topic(env.RFID))
    MQTTC.subscribe(common.get_topic(env.LCD))
    MQTTC.subscribe(common.get_topic(env.BUTTON))
# publish all data in the Queue
def execute_publications():
    while True:
        topic, payload, qos = message_queue.get()
        MQTTC.publish(topic, payload, qos)
    
def disconnect():
    MQTTC.disconnect()

def loop_stop():
    MQTTC.loop_stop()