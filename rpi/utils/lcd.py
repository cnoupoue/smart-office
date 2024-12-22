#!/usr/bin/env python
from grovepi import *
from grove_rgb_lcd import *

def set_rgb(r, g, b):
    try:
        setRGB(r, g, b)
    except (IOError,TypeError) as e:
        print("Error" + str(e))
def set_text(text):
    try:
        setText(text)
    except (IOError,TypeError) as e:
        print("Error" + str(e))