import controllers.common as common
import utils.button as button
import env
import controllers.mqtt_controller as mqtt_controller

def read(BUTTON_QUEUE, button_old_value, set_button_old_value):
    button_value = button.read()
    avg_button_value = 0
    # filter not valid data
    if button_value <= 1:
        BUTTON_QUEUE.append(button_value)
        # calculation for more accuracy based on previous values
        avg_button_value = sum(BUTTON_QUEUE) / len(BUTTON_QUEUE)
        # logic to detect pressed action once
        if avg_button_value >= 0.5 and button_old_value == 0:
            mqtt_controller.publish(env.BUTTON, "PRESSED")
            set_button_old_value(1)
            print("PRESSED")
        elif avg_button_value < 0.5 and button_old_value == 1:
            set_button_old_value(0)

