#!/usr/bin/env python
import grovepi

# to digital port D4
pin = 4

grovepi.pinMode(pin,"OUTPUT")

def on():
    try:
        grovepi.digitalWrite(pin,1)
    except IOError:
        print ("Error")

def off():
    try:
        grovepi.digitalWrite(pin,0)
    except IOError:
        print ("Error")