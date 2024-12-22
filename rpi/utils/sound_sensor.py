#!/usr/bin/env python
import grovepi

# to analog port A0
sound_sensor = 1

grovepi.pinMode(sound_sensor,"INPUT")

def read():
    try:
        return grovepi.analogRead(sound_sensor)
    except IOError:
        print ("Error")
