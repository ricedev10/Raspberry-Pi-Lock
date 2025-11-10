from machine import I2C, Pin
from library.pico_i2c_lcd import I2cLcd
from utime import sleep
from enum import Enum

# Configuration
INPUT_CODE_MESSAGE = "Enter 4-digit code:"
GREETING_MESSAGE = ("Welcome to", "Keylock PRO")
INCORRECT_MESSAGE = ("Incorrect!", "Enter code:")

HOLD_DURATION = 2.0 # if user holds the button for 2+ seconds, they can change keycode
keycode = [0, 0, 0, 0]  # user *must* press the corresponding buttons in this order, Note: user can change this

# Buttons
keypad_buttons = [  # replace [__] with the pin numbers
    Pin(00, Pin.IN, Pin.PULL_UP),
    Pin(01, Pin.IN, Pin.PULL_UP),
    Pin(02, Pin.IN, Pin.PULL_UP),
    Pin(03, Pin.IN, Pin.PULL_UP),
]

# LEDs -- make sure each led corresponds to the buttons above
keypad_LEDs = [
    Pin(00, Pin.OUT),
    Pin(01, Pin.OUT),
    Pin(02, Pin.OUT),
    Pin(03, Pin.OUT),
]

# LCD Display
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000) #Data pin is pin 0, clock pin is pin 1
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16) 

# user input variables
current_keycode = []
current_inputs = 0 # for keeping track of syncing the state while "sleeping"

# LCD display helper functions
def write_to_display(message: str | tuple[str, str]):
    lcd.clear()
    if message is str:
        lcd.putstr(line1)
    else:
        lcd.putstr(message[0])
        lcd.move_to(0, 1)
        lcd.putstr(message[1])
def clear_display():
    lcd.clear()

# keycode helper functions
def is_correct_keycode() -> bool:
    return current_keycode == keycode

def reset_keycode() -> None:
    current_keycode = []


# Event functions
def on_entering_keycode():
    reset_keycode()

    if is_correct_keycode():
        # TODO: open drawer

        pass
    else:
        # display incorrect
        input_now = current_inputs
        write_to_display(INCORRECT_MESSAGE)
        sleep(2.0)
        if input_now == current_inputs:
            clear_display()
            write_to_display(INPUT_CODE_MESSAGE)

def on_button_start_holding(id: int):
    keypad_LEDs[id].on() # start the LED to light up

def on_button_pressed(id: int):
    # on pressing button...
        # 1. Keep track of user inputted keycode
        # 2. Turn the led back off
    current_keycode.append(id)
    keypad_LEDs[id].off()

    if len(current_keycode) == len(keycode):
        # we have entered maximum digits and inputted keycode
        on_entering_keycode()


# Initialize program
write_to_display(GREETING_MESSAGE)
sleep(1)
write_to_display(INPUT_CODE_MESSAGE)

# Connect button functions to event
for i in range(0, len(keypad_buttons) - 1):
    button = keypad_buttons[i]
    def on_pressed(_pin: Pin):
        on_button_pressed(i)
    def on_hold_start(_pin: Pin):
        on_button_start_holding(i)

    button.irq(trigger=Pin.IRQ_RISING, handler=on_pressed)
    button.irq(trigger=Pin.IRQ_FALLING, handler=on_hold_start)

# Main loop can now do other things
while True:
    sleep(1)
