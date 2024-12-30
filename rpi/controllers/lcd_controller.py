import controllers.common as common
import utils.lcd as lcd

def clear():
    common.set_lcd_values("", 0, 0, 0)

def display_info(msg):
    common.set_lcd_values(msg, 0, 50, 255)

def display_success(msg):
    common.set_lcd_values(msg, 0, 150, 0)

def display_error(msg):
    common.set_lcd_values(msg, 255, 0, 0)

def display_warning(msg):
    common.set_lcd_values(msg, 255, 200, 0)

def set(msg, r, g, b):
    lcd.set_rgb(r, g, b)
    lcd.set_text(msg)