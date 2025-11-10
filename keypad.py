from machine import Pin
from utime import sleep

# Configuration
keycode = [0, 0, 0, 0]  # user *must* press the corresponding buttons in this order

# Buttons
keypad_buttons = [  # replace [__] with the pin numbers
    Pin(00, Pin.IN, Pin.PULL_UP),
    Pin(01, Pin.IN, Pin.PULL_UP),
    Pin(02, Pin.IN, Pin.PULL_UP),
    Pin(03, Pin.IN, Pin.PULL_UP),
]
input_button = Pin(05, Pin.IN, Pin.PULL_UP) # this button is for entering/changing keypad code

# LEDs -- make sure each led corresponds to the buttons above
keypad_LEDs = [
    Pin(00, Pin.OUT),
    Pin(01, Pin.OUT),
    Pin(02, Pin.OUT),
    Pin(03, Pin.OUT),
]

# user input variables
current_keycode = []

# Event functions
def on_button_press(id):
    # on pressing button...
        # 1. Keep track of user inputted code
        # 2. Light up the led
    current_keycode.append(id)
    keypad_LEDs[id].on()


# Attach interrupt to trigger on a falling edge (button press)
for i in range(0, len(keypad_buttons) - 1):
    button = keypad_buttons[i]
    button.irq(trigger=Pin.IRQ_RISING, handler=on_button_press)

# Main loop can now do other things
while True:
    sleep(1)
