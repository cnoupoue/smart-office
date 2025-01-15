import controllers.common as common
import utils.button as button
import env
import controllers.mqtt_controller as mqtt_controller
import time

last_read = 0

def run(BUTTON_QUEUE, button_old_value, set_button_old_value):
    global last_read
    button_value = button.read()
    avg_button_value = 0
    ready = time.time() - last_read >= env.BUTTON_DELAY

    # filter not valid data
    if button_value <= 1:
        BUTTON_QUEUE.append(button_value)
        # calculation for more accuracy based on previous values
        avg_button_value = sum(BUTTON_QUEUE) / len(BUTTON_QUEUE)
        # logic to detect pressed action once
        if avg_button_value >= 0.5 and button_old_value == 0 and ready:
            last_read = time.time()
            mqtt_controller.put_in_publish_queue(env.BUTTON, "PRESSED")
            set_button_old_value(1)
            print("PRESSED")
        elif avg_button_value < 0.5 and button_old_value == 1 and ready:
            last_read = time.time()
            set_button_old_value(0)