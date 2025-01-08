import controllers.common
import utils.gps as gps
import utils.geocode as geocode
import time
import env
import controllers.mqtt_controller as mqtt_controller
import json

def run():
    print("gps init")
    while True:
        value = gps.read_coordinates()
        if value == None:
            continue
        [lat,lon] = value
        address: dict = geocode.getAdress(lat,lon)
        address["lat"] = lat
        address["lon"] = lon
        mqtt_controller.publish(env.GPS, json.dumps(address))
        print("gps: " + str(list(address.values())))
        time.sleep(env.GPS_DELAY)