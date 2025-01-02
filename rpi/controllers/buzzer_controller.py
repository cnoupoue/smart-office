import controllers.common as common
import time
import utils.buzzer as buzzer
import threading
import os

def get_buzzer_alarm_state():
    return str(os.environ.get("buzzer_state", 0))

def set_buzzer_alarm_state(value):
    os.environ["buzzer_state"] = str(value)

def start():
    threading.Thread(target=_start).start()

def _start():
    set_buzzer_alarm_state(1)
    while get_buzzer_alarm_state() == "1":
        common.set_buzzer(1)
        time.sleep(1)
        common.set_buzzer(0)
        time.sleep(1)

def stop():
    set_buzzer_alarm_state(0)

def three_quick_bip():
    common.set_buzzer(1)
    time.sleep(0.1)
    common.set_buzzer(0)
    time.sleep(0.1)
    common.set_buzzer(1)
    time.sleep(0.1)
    common.set_buzzer(0)
    time.sleep(0.1)
    common.set_buzzer(1)
    time.sleep(0.1)
    common.set_buzzer(0)
    time.sleep(0.1)