import os
import controllers.common
import env
from utils.mqtt import MQTT

def update_rpi_id():
    mqttc = MQTT(client_id=env.CLIENT_Id, sub_callback = set_premise)
    mqttc.connect(url=env.BROKER, port=env.PORT)
    _ask_for_premise(mqttc)
    _listen_to_premise(mqttc)

def get_serial_number():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if line.startswith('Serial'):
                    return line.strip().split(': ')[1]
    except FileNotFoundError:
        return None

def set_premise(value: str) -> None:
    os.environ[env.PREMISE_ENV_VAR_NAME] = value

def get_premise():
    return os.environ.get(env.PREMISE_ENV_VAR_NAME, "null")

def _ask_for_premise(mqttc: MQTT):
    t = env.INITIAL_TOPIC
    mqttc.publish(topic=t, value=get_serial_number())

def _listen_to_premise(mqttc: MQTT):
    t = env.MQTT_TOPIC_ROOT + env.DEF_COMPANY_ID + get_serial_number()
    mqttc.subscribe(topic=t)