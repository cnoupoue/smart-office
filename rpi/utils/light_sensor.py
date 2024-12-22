#!/usr/bin/env python
import grovepi

# to port A0
light_sensor = 0

grovepi.pinMode(light_sensor,"INPUT")

def read():
    try:
        return grovepi.analogRead(light_sensor)
    except IOError:
        print ("Error")
        return None
