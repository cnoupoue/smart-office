import controllers.mqtt_controller as mqtt_controller
import signal
import sys

import controllers.multi_sensor_controller as multi_sensor_controller
import controllers.camera_controller as camera_controller
import controllers.gps_controller as gps_controller
import controllers.rfid_controller as rfid_controller
import controllers.hello_controller as hello_controller
import controllers.common as common
import threading
import time
import env

# variables initialisation
common.init_serial_number()

# essential thread initialisation
t_multi_sensor_controller = threading.Thread(target=multi_sensor_controller.run).start()

try:
    # MQTT initialisation
    mqtt_controller.init()
except Exception as e:
    print("ERROR")
# Asking to client_server for premise
mqtt_controller.ask_for_premise()

# The RaspberryPi wait until it receives its premise 
print("waiting for premise to be assigned by the server")
while(not common.get_premise()):
    time.sleep(env.HELLO_DELAY)

# Threads initialisation
t_camera = threading.Thread(target=camera_controller.run).start()
t_gps = threading.Thread(target=gps_controller.run).start()
t_rfid = threading.Thread(target=rfid_controller.run).start()
t_hello = threading.Thread(target=hello_controller.run).start()

# Run publish task
mqtt_controller.subscribeToOtherTopics()
mqtt_controller.execute_publications()

# register CTRL + C signal
def signal_handler(sig, frame):
    print("Disconnecting from MQTT broker...")
    mqtt_controller.disconnect()
    mqtt_controller.loop_stop()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

while True:
    time.sleep(env.HELLO_DELAY)