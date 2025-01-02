#!/usr/bin/env python
import grovepi

# to port A1
light_sensor = 1

grovepi.pinMode(light_sensor,"INPUT")

def read():
    try:
        return grovepi.analogRead(light_sensor)
    except Exception  as e:
        print(f"Error reading sensor: {e}")
        return None
