#!/usr/bin/env python
import time
import grovepi

pin = 8
grovepi.pinMode(pin,"OUTPUT")

def on():
    try:
        grovepi.digitalWrite(pin,1)
    except KeyboardInterrupt as e:
        grovepi.digitalWrite(pin,0)
        print ("Error: " + e)
    except IOError as e:
        print ("Error: " + e)

def off():
    try:
        grovepi.digitalWrite(pin,0)
    except KeyboardInterrupt as e:
        grovepi.digitalWrite(pin,0)
        print ("Error: " + e)
    except IOError as e:
        print ("Error: " + e)