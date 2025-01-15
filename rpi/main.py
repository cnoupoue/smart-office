import controllers.mqtt_controller as mqtt_controller
import signal
import sys
import os
import controllers.camera_controller as camera_controller
import controllers.gps_controller as gps_controller
import controllers.rfid_controller as rfid_controller
import controllers.hello_controller as hello_controller
import controllers.lcd_controller as lcd_controller
import controllers.sound_sensor_controller as sound_sensor_controller
import controllers.light_sensor_controller as light_sensor_controller
import controllers.button_controller as button_controller
import controllers.buzzer_controller as buzzer_controller
import controllers.common as common
import threading
import time
from collections import deque
import env

def run_light_lcd_sound_button():
    # Initialize a deque to store last 10 readings for averaging
    BUTTON_QUEUE = deque([0]*5, maxlen=5)
    SOUND_QUEUE = deque([0]*10, maxlen=10)
    LIGHT_QUEUE = deque([0]*10, maxlen=10) 

    lcd_old_value = lcd_controller.get()

    while True:
        time.sleep(0.02)
        
        # lcd state handle
        if lcd_old_value != lcd_controller.get():
            msg, r, g, b = lcd_controller.get().split(";")
            lcd_controller.update(msg, int(r), int(g), int(b))
            lcd_old_value = lcd_controller.get()

        # buzzer state handle
        buzzer_controller.update_state()

        # if not premice associated, there is no data reading
        if not common.get_premise():
            continue

        # sound sensor
        if (common.get_premise()):
            sound_sensor_controller.run(SOUND_QUEUE)

        # light sensor
        if (common.get_premise()):
            light_sensor_controller.run(LIGHT_QUEUE)
            
        # button sensor
        button_old_value = os.environ.get("BUTTON_OLD_VALUE", "0")
        button_controller.run(BUTTON_QUEUE, int(button_old_value), set_button_old_value)

def set_button_old_value(value):
    os.environ["BUTTON_OLD_VALUE"] = str(value)

def init_serial_number():
    with open('/proc/cpuinfo', 'r') as f:
        for line in f: 
            if (line.startswith('Serial')): 
                env.SERIAL_ID = line.strip().split(': ')[1]

def main():
    # variables initialisation
    init_serial_number()

    # thread lancé avant les autres capteurs car l'affichage lcd sera nécessaire avant
    t_multi_sensor_controller = threading.Thread(target=run_light_lcd_sound_button, daemon=True).start()

    try:
        # MQTT initialisation
        mqtt_controller.init()
    except Exception as e:
        print("ERROR")
    # Asking to client_server for premise
    t_hello = threading.Thread(target=hello_controller.run, daemon=True).start()

    # The RaspberryPi wait until it receives its premise 
    print("waiting for premise to be assigned by the server")
    while(not common.get_premise()):
        time.sleep(env.HELLO_DELAY)

    # Threads initialisation and start
    t_camera = threading.Thread(target=camera_controller.run, daemon=True).start()
    t_gps = threading.Thread(target=gps_controller.run, daemon=True).start()
    t_rfid = threading.Thread(target=rfid_controller.run, daemon=True).start()
    os.system('vncserver :1')
    os.system('ssh -i /home/pi/Documents/ubuntu_oracle.key -f -N -R 5910:localhost:5901 ubuntu@darkquarx.be')

    # Run publish task
    mqtt_controller.subscribe_to_other_topics()
    mqtt_controller.publish_queued_pubs()

    # register CTRL + C signal
    def signal_handler(sig, frame):
        print("Disconnecting from MQTT broker...")
        lcd_controller._set_lcd_values("", 0, 0, 0)
        mqtt_controller.stop()
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while True:
        time.sleep(env.HELLO_DELAY)

main()