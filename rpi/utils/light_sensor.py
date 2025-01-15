#!/usr/bin/env python
import grovepi

# to port A1
pin = 1

grovepi.pinMode(pin,"INPUT")

def read():
    try:
        return grovepi.analogRead(pin)
    except Exception  as e:
        print(f"Error reading sensor: {e}")
        return None
