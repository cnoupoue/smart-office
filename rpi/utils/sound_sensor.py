#!/usr/bin/env python
import grovepi

# to analog port A0
pin = 0

grovepi.pinMode(pin,"INPUT")

def read():
    try:
        return grovepi.analogRead(pin)
    except Exception  as e:
        print(f"Error reading sensor: {e}")
        return None
