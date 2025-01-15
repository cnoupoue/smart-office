import controllers.common as common
import time
import env
import utils.sound_sensor as sound_sensor
import controllers.mqtt_controller as mqtt_controller

# the max value i got when putting a light source behind
SOUND_MAX_VALUE = 1000 
last_read = 0

def run(SOUND_QUEUE):
    global last_read
    sound_value = sound_sensor.read()
    avg_sound_value = 0
        # filter not valid data
        # and only send if 2 seconds passed
    ready = time.time() - last_read >= env.SOUND_SENSOR_DELAY
    if sound_value < SOUND_MAX_VALUE and ready:
        last_read = time.time()
        SOUND_QUEUE.append(sound_value)
            # calculation for more accuracy based on previous values
        avg_sound_value = sum(SOUND_QUEUE) / len(SOUND_QUEUE)
        mqtt_controller.put_in_publish_queue(env.SOUND_SENSOR, avg_sound_value)
        print("sound: " + str(avg_sound_value))