#!/usr/bin/env python
import grovepi

# to port D7
pin = 7

grovepi.pinMode(pin,"INPUT")

def read():
    try:
        return grovepi.digitalRead(pin)
    except IOError as e:
        print ("Error: " + str(e))
        return None