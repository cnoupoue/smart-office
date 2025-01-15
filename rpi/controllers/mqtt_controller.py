import os
import controllers.common as common
import env
from utils.mqtt import MQTT
import controllers.lcd_controller as lcd_controller
import controllers.buzzer_controller as buzzer_controller
import utils.ip as ip
import time
import queue

MQTTC : MQTT = None
message_queue = queue.Queue()
INIT_STATUS = True

def init():
    lcd_controller.display_info("Demarrage de \nl'appareil...")
    global MQTTC
    MQTTC = MQTT(sub_callback = _manage_subscribed_topics)
    retry = True
    while(not ip.read()):
        lcd_controller.display_error("En attente de \nconnexion reseau")
        time.sleep(2)
    while(retry):
        try:
            MQTTC.connect(url=env.BROKER, port=env.PORT)
            retry = False
        except Exception as e:
            print("GOT: " + str(e) + ",\nTry to reconnect in 2 seconds")
            retry = True
            time.sleep(2)
            lcd_controller.display_error("En attente de\nBroker...")
    MQTTC.subscribe(_get_absolute_topic(env.HELLO), 2)
    MQTTC.subscribe(_get_absolute_topic(env.YOU_ARE))

# ask to server the premise
def ask_for_premise():
    MQTTC.publish(_get_absolute_topic(env.HELLO), env.SERIAL_ID, 2)

# define different actions depending on the received message
def _manage_subscribed_topics(topic: str, value: str) -> None:
    global INIT_STATUS
    print(topic + " : " + value)
    if topic == _get_absolute_topic(env.YOU_ARE):
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
            if old_premise != value:
                lcd_controller.display_info("Mon local est: \n" + value)
            time.sleep(0.5)
        common.set_premise(value)
    # subscribed to my own to ensure that mqtt is started and then display the message, (haven't found other solutions)
    elif topic == _get_absolute_topic(env.HELLO):
        if (common.get_premise() is None and INIT_STATUS):
            lcd_controller.display_warning("Recherche serveur en cours...")
    elif common.get_premise() == None:
        # if local is not defined, it means that, raspberry hasn't contacted the server yet
        return
    elif topic == _get_absolute_topic(env.RFID):
        print("RFID LISTENED")
        buzzer_controller.three_quick_bip()
        put_in_publish_queue(env.RELAY, "ON_OFF:5")
    elif topic == _get_absolute_topic(env.BUZZER):
        if value == "ON":
            buzzer_controller.start_alarm()
        if value == "OFF":
            buzzer_controller.stop()
    elif topic == _get_absolute_topic(env.LCD):
        if not value.startswith("ERROR"):
            return
        type,message = value.split(";")
        if type == "ERROR":
            buzzer_controller.start_alarm()
            lcd_controller.display_error(message)
    elif topic == _get_absolute_topic(env.BUTTON):
        lcd_controller.display_info("Mon local est: \n" + common.get_premise())
        buzzer_controller.stop()
    else:
        print("Unknown topic")

# put publication data in a Queue, to publish in order
def put_in_publish_queue(topic: str, payload, qos=0):
    # if topic starts with "smartoffice/", it's a full topic path.
    # but if it starts with something else, it's a relative topic path
    if topic.startswith(env.MQTT_ROOT_TOPIC):
        message_queue.put((topic, payload, qos))
    else:
        message_queue.put((_get_absolute_topic(topic), payload, qos))

def subscribe_to_other_topics():
    MQTTC.subscribe(_get_absolute_topic(env.BUZZER))
    MQTTC.subscribe(_get_absolute_topic(env.RFID))
    MQTTC.subscribe(_get_absolute_topic(env.LCD))
    MQTTC.subscribe(_get_absolute_topic(env.BUTTON))
# publish all data in the Queue
def publish_queued_pubs():
    while True:
        topic, payload, qos = message_queue.get()
        retain = False
        if topic.endswith("gps"):
            retain=True
        MQTTC.publish(topic, payload, qos, retain)

def _disconnect():
    MQTTC.disconnect()

def _loop_stop():
    MQTTC.loop_stop()

def stop():
    _disconnect()
    _loop_stop()

def _get_absolute_topic(sensor: str):
    rpi_id = env.SERIAL_ID + "/"
    return  env.MQTT_ROOT_TOPIC + env.DEF_COMPANY_ID + rpi_id + sensor