#!/usr/bin/env python
import time
import grovepi

buzzer = 8
grovepi.pinMode(buzzer,"OUTPUT")

def on():
    try:
        grovepi.digitalWrite(buzzer,1)
    except KeyboardInterrupt as e:
        grovepi.digitalWrite(buzzer,0)
        print ("Error: " + e)
    except IOError as e:
        print ("Error: " + e)

def off():
    try:
        grovepi.digitalWrite(buzzer,0)
    except KeyboardInterrupt as e:
        grovepi.digitalWrite(buzzer,0)
        print ("Error: " + e)
    except IOError as e:
        print ("Error: " + e)