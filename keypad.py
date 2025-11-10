from machine import I2C, Pin
from library.pico_i2c_lcd import I2cLcd
from utime import sleep
import neopixel

# Configuration
INPUT_CODE_MESSAGE = "Enter code: "
GREETING_MESSAGE = ("Welcome to", "Keylock PRO")
INCORRECT_MESSAGE = ("Incorrect!", "Try Again")
OPENING_DRAWER_MESSAGE = "Opening..."
OPENED_DRAWER_MESSAGE = ("Close: >", "Open: >")
CENSORED_KEY = "*"  # displays on LCD when inputting keycode

RESET_PIN = 0  # corresponds to the index of the keypad_buttons
TOGGLE_DRAWER_PIN = 1  # corresponds to the index of the keypad_buttons

BUTTON_COLORS = [
    (255, 165, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 25),  # Green
    (0, 0, 255),  # Blue
]

HOLD_DURATION = 2.0  # if user holds the button for 2+ seconds, they can change keycode
keycode = [
    0,
    0,
    0,
    0,
]  # user *must* press the corresponding buttons in this order, Note: user can change this

# Buttons
keypad_buttons = [  # replace [__] with the pin numbers
    Pin(15, Pin.IN, Pin.PULL_UP),
    Pin(14, Pin.IN, Pin.PULL_UP),
    Pin(13, Pin.IN, Pin.PULL_UP),
    Pin(12, Pin.IN, Pin.PULL_UP),
]

# LEDs -- set up initial color of each pixel
leds = neopixel.NeoPixel(Pin(00), len(keypad_buttons))
for i in range(len(BUTTON_COLORS)):
    leds[i] = (0, 0, 0)  # initially have all the LEDs "off"


def led_on(id):
    leds[id] = BUTTON_COLORS[id]


def led_off(id):
    leds[id] = (0, 0, 0)


# LCD Display
i2c = I2C(
    0, sda=Pin(0), scl=Pin(1), freq=400000
)  # Data pin is pin 0, clock pin is pin 1
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

# user input variables
current_keycode = []
new_keycode = []
current_inputs = 0  # for keeping track of syncing the state while "sleeping"
can_enter_keycode = True
is_resetting_keycode = False


# LCD display helper functions
def append_to_display(message: str):
    lcd.putstr(message)


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
def toggle_drawer():
    # TODO: code for opening/closing the drawer via the servo/motor
    pass


def reset_pin():
    global can_enter_keycode, is_resetting_keycode

    can_enter_keycode = False
    is_resetting_keycode = True
    reset_keycode()
    write_to_display(("Enter new keycode..."))
    can_enter_keycode = True


def on_entering_keycode():
    global can_enter_keycode, is_resetting_keycode, keycode

    can_enter_keycode = False
    if is_resetting_keycode:
        if len(new_keycode) > 0:
            if new_keycode == keycode:
                keycode = new_keycode
                keycode = new_keycode
                write_to_display(("Successfully", "changed keycode"))
            else:
                write_to_display("")
        else:
            write_to_display("ERROR")

    reset_keycode()

    if is_correct_keycode():
        toggle_drawer()
        write_to_display(OPENING_DRAWER_MESSAGE)
        print("waiting for drawer to open")
        sleep(4.0)  # wait for drawer to open
        write_to_display(OPENED_DRAWER_MESSAGE)
        print("opened drawer")
    else:
        # display incorrect
        input_now = current_inputs
        write_to_display(INCORRECT_MESSAGE)
        sleep(2.0)
        if input_now == current_inputs:
            clear_display()
            write_to_display(INPUT_CODE_MESSAGE)

    print("can close/reset drawer")
    can_enter_keycode = True


def on_button_start_holding(id: int):
    led_on(id)  # start the LED to light up


def on_button_pressed(id: int):
    # update events
    if not can_enter_keycode:
        if id == RESET_PIN:
            reset_pin()
        elif id == TOGGLE_DRAWER_PIN:
            toggle_drawer()
        return

    # on pressing button...
    # 1. Keep track of user inputted keycode
    # 2. Turn the led back off
    # 3. Update LCD display of censored digits
    current_keycode.append(id)
    led_off(id)
    append_to_display(CENSORED_KEY)

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
