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
        try:
            value = gps.read_coordinates()
            if value == None:
                continue
            [lat,lon] = value
            address: dict = geocode.get_address(lat,lon)
            address["lat"] = lat
            address["lon"] = lon
            mqtt_controller.put_in_publish_queue(env.GPS, json.dumps(address))
            print("gps: " + str(list(address.values())))
            time.sleep(env.GPS_DELAY)
        except Exception as e:
            print(str(e))

def test():
    address: dict = geocode.get_address("50.620788", "5.581412")
    address["lat"] = "50.620788"
    address["lon"] = "5.581412"
    print(json.dumps(address))



    