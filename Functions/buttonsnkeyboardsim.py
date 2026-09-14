import Functions.buttons as button
from Functions.keyboard_simulation import type_string, press_key, setup_gadget

def run():
    while True:
        if button.button1():
            type_string("a")
        if button.button2():
            type_string("s")
        if button.button4():
            type_string("k")
        if button.button5():
            type_string("l")



