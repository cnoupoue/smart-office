import controllers.common as common
import utils.buzzer as buzzer
import time
import threading
import os
import env

def _get_buzzer_alarm_state():
    return str(os.environ.get("buzzer_state", 0))

def _activate_alarm_state(value:bool):
    os.environ["buzzer_state"] = str(1 if value else 0)

def start_alarm():
    threading.Thread(target=_start_alarm).start()

def _start_alarm():
    _activate_alarm_state(True)
    while _get_buzzer_alarm_state() == "1":
        _set_buzzer(1)
        time.sleep(1)
        _set_buzzer(0)
        time.sleep(1)

def stop():
    _activate_alarm_state(False)

def three_quick_bip():
    _set_buzzer(1)
    time.sleep(0.1)
    _set_buzzer(0)
    time.sleep(0.1)
    _set_buzzer(1)
    time.sleep(0.1)
    _set_buzzer(0)
    time.sleep(0.1)
    _set_buzzer(1)
    time.sleep(0.1)
    _set_buzzer(0)
    time.sleep(0.1)


def update_state():
    if _get_buzzer() == "1":
        buzzer.on()
    else:
        buzzer.off()

def _get_buzzer():
    return str(os.environ.get(env.BUZZER, 0))

def _set_buzzer(value):
    os.environ[env.BUZZER] = str(value)