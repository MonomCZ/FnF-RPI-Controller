import Functions.gpio_buttons as button
from Functions.keyboard_simulation import type_string, press_key, setup_gadget

def run():
    while True:
        if button.button1():
            press_key(0x00,0x04) #a
        if button.button2():
            press_key(0x16) #s
        if button.button4():
            press_key(0x00,0x0e) #k
        if button.button5():
            press_key(0x00,0x0f) #l



