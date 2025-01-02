#!/usr/bin/env python
import grovepi

# to digital port D4
led = 4

grovepi.pinMode(led,"OUTPUT")

def on():
    try:
        grovepi.digitalWrite(led,1)
    except IOError:
        print ("Error")

def off():
    try:
        grovepi.digitalWrite(led,0)
    except IOError:
        print ("Error")