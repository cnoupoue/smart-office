import sys

sys.path.append('..')

import env

import controllers.premise_controller as premise_controller

def get_topic(sensor: str):
    premise = premise_controller.get_premise() + "/"
    return  env.MQTT_TOPIC_ROOT + env.DEF_COMPANY_ID + premise + sensor