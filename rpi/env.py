# PROCESS TIME
HELLO_DELAY = 10 # each x seconds, check the premise
LIGHT_SENSOR_DELAY = 2
SOUND_SENSOR_DELAY = 2
GPS_DELAY = 60
CAMERA_HELLO_DELAY = 5
BUTTON_DELAY = 0.02

# MQTT BROKER
BROKER = "smartoffice-company1.local"
# BROKER = "broker.hivemq.com"
CLIENT_ID = "1"
PORT = 1883

# ENV VARIABLES
PREMISE_ENV_VAR_NAME = 'SMARTOFFICE_PREMISE'
LCD_ENV_VAR_NAME = 'LCD_VAR'
SERIAL_ID = None

# MQTT TOPIC
MQTT_ROOT_TOPIC = "smartoffice/"
DEF_COMPANY_ID = "1/"

# TOPIC/SENSOR TYPE
HELLO = "hello"
YOU_ARE = "youare"
LIGHT_SENSOR = "light_sensor"
SOUND_SENSOR = "sound_sensor"
CAMERA = "camera"
GPS = "gps"
BUTTON = "button"
BUZZER = "buzzer"
LCD = "lcd"
RFID = "rfid"
RELAY = "relay"
