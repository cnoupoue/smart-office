import controllers.common as common
import utils.lcd as lcd
import os
import env

def display_info(msg):
    _set_lcd_values(msg, 0, 50, 255)

def display_success(msg):
    _set_lcd_values(msg, 0, 150, 0)

def display_error(msg):
    _set_lcd_values(msg, 255, 0, 0)

def display_warning(msg):
    _set_lcd_values(msg, 255, 200, 0)

def update(msg, r, g, b):
    lcd.set_rgb(r, g, b)
    lcd.set_text(msg)

def get():
    return os.environ.get(env.LCD_ENV_VAR_NAME, None)

def _set_lcd_values(msg, r, g, b):
    os.environ[env.LCD_ENV_VAR_NAME] = f"{msg};{r};{g};{b}"