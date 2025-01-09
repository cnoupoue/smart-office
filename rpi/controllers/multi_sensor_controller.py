import controllers.common as common
import time
import os
import env
import utils.buzzer as buzzer
import controllers.lcd_controller as lcd_controller
import controllers.sound_sensor_controller as sound_sensor_controller
import controllers.light_sensor_controller as light_sensor_controller
import controllers.button_controller as button_controller
from collections import deque

# Initialize a deque to store last 10 readings for averaging
BUTTON_QUEUE = deque([0]*5, maxlen=5)
SOUND_QUEUE = deque([0]*10, maxlen=10)
LIGHT_QUEUE = deque([0]*10, maxlen=10) 


lcd_old_value = common.get_lcd()

def run():
    lcd_old_value = common.get_lcd()

    while True:
        time.sleep(0.02)
        
        # lcd state handle
        if lcd_old_value != common.get_lcd():
            msg, r, g, b = common.get_lcd().split(";")
            lcd_controller.set(msg, int(r), int(g), int(b))
            lcd_old_value = common.get_lcd()

        # buzzer state handle
        if common.get_buzzer() == "1":
            buzzer.on()
        else:
            buzzer.off()

        # if not premice associated, there is no data reading
        if not common.get_premise():
            continue

        # sound sensor
        sound_sensor_controller.read(SOUND_QUEUE)

        # light sensor
        light_sensor_controller.read(LIGHT_QUEUE)
            
        # button sensor
        button_old_value = os.environ.get("BUTTON_OLD_VALUE", "0")
        button_controller.read(BUTTON_QUEUE, int(button_old_value), set_button_old_value)

def set_button_old_value(value):
    os.environ["BUTTON_OLD_VALUE"] = str(value)
