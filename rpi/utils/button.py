#!/usr/bin/env python
import grovepi

# to port D7
button = 7

grovepi.pinMode(button,"INPUT")

def read():
    try:
        return grovepi.digitalRead(button)
    except IOError as e:
        print ("Error: " + str(e))
        return None