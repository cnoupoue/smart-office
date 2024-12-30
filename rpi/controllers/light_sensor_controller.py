import controllers.common as common
import time
import env
import utils.light_sensor as light_sensor
import controllers.mqtt_controller as mqtt_controller


# the max value i got when putting a light source behind
LIGHT_MAX_VALUE = 800 

def read(COUNTER, LIGHT_QUEUE):
    light_value = light_sensor.read()
    avg_light_value = 0
    # filter not valid data
    # and only send if 2 seconds passed
    if light_value < LIGHT_MAX_VALUE and COUNTER == 0:
        LIGHT_QUEUE.append(light_value)
        # calculation for more accuracy based on previous values
        avg_light_value = sum(LIGHT_QUEUE) / len(LIGHT_QUEUE)
        mqtt_controller.publish(env.LIGHT_SENSOR, avg_light_value)
        print("light: " + str(avg_light_value))
