import sys
import os

sys.path.append('..')

import env

def get_topic(sensor: str):
    rpi_id = env.SERIAL_ID + "/"
    return  env.MQTT_ROOT_TOPIC + env.DEF_COMPANY_ID + rpi_id + sensor

def init_serial_number():
    with open('/proc/cpuinfo', 'r') as f:
        for line in f: 
            if (line.startswith('Serial')): 
                env.SERIAL_ID = line.strip().split(': ')[1]
                env.HELLO_TOPIC = env.MQTT_ROOT_TOPIC + env.DEF_COMPANY_ID + env.SERIAL_ID + "/" + "hello"
                env.YOU_ARE_TOPIC = env.MQTT_ROOT_TOPIC + env.DEF_COMPANY_ID + env.SERIAL_ID + "/" + "youare"

def get_premise():
    value = os.environ.get(env.PREMISE_ENV_VAR_NAME, None)
    return value if value != "NONE" else None

def set_premise(value):
    os.environ[env.PREMISE_ENV_VAR_NAME] = value

def get_lcd():
    return os.environ.get(env.LCD_ENV_VAR_NAME, None)

def set_lcd_values(msg, r, g, b):
    os.environ[env.LCD_ENV_VAR_NAME] = f"{msg};{r};{g};{b}"

def get_buzzer():
    return str(os.environ.get(env.BUZZER, 0))

def set_buzzer(value):
    os.environ[env.BUZZER] = str(value)