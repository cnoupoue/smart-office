#!/usr/bin/env python
import grove_rgb_lcd

def set_rgb(r, g, b):
    try:
        grove_rgb_lcd.setRGB(r, g, b)
        return 0
    except (IOError,TypeError) as e:
        print("Error: " + str(e))
        return -1
def set_text(text):
    try:
        grove_rgb_lcd.setText(text)
        return 0
    except (IOError,TypeError) as e:
        print("Error: " + str(e))
        return -1
