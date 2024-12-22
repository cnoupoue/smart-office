# MQTT BROKER
BROKER = "broker.hivemq.com"
CLIENT_ID = "id1"
PORT = 1883

# MQTT TOPIC
MQTT_TOPIC_ROOT = "smartoffice/"
DEF_COMPANY_ID = "id1/"
def_local = "null/"
def_sensor = "rpi/"
INITIAL_TOPIC = MQTT_TOPIC_ROOT + DEF_COMPANY_ID + def_local + def_sensor

# ENV VARIABLES
PREMISE_ENV_VAR_NAME = 'SMARTOFFICE_PREMISE'

# SENSOR TYPE
LIGHT_SENSOR = "light_sensor"
SOUND_SENSOR = "sound_sensor"
CAMERA = "camera"
GPS = "gps"
BUTTON = "button"
BUZZER = "buzzer"
LCD = "lcd"
TEMPERATURE = "temperature"
LED = "led"
RELAY = "relay"