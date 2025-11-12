from machine import Pin, I2C, PWM
from time import sleep
import neopixel
from pico_i2c_lcd import I2cLcd

# =====================
# --- MOTOR SETUP ---
# =====================
ina1 = Pin(18, Pin.OUT)
ina2 = Pin(17, Pin.OUT)
pwma = PWM(Pin(16))
pwma.freq(1000)


def RotateCW(duty):
    """Rotate motor clockwise at specified duty cycle (0-100)"""
    ina1.value(1)
    ina2.value(0)
    duty_16 = int((duty * 65536) / 100)
    pwma.duty_u16(duty_16)


def RotateCCW(duty):
    """Rotate motor counter-clockwise at specified duty cycle (0-100)"""
    ina1.value(0)
    ina2.value(1)
    duty_16 = int((duty * 65536) / 100)
    pwma.duty_u16(duty_16)


def StopMotor():
    """Stop the motor completely"""
    ina1.value(0)
    ina2.value(0)
    pwma.duty_u16(0)


StopMotor()  # make sure motor is not initially running

# =====================
# --- LCD SETUP ---
# =====================
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
lcd.clear()
lcd.putstr("Enter Code:")

# =====================
# --- LED SETUP (NeoPixel strip) ---
# =====================
n = 8  # number of LEDs (only 4 used)
p = 2  # GPIO pin connected to NeoPixel
np = neopixel.NeoPixel(Pin(p), n)

# LED color map: (R, G, B)
LED_COLORS = {
    "B": (0, 0, 255),  # Blue
    "W": (255, 255, 255),  # White
    "R": (255, 0, 0),  # Red
    "Y": (255, 255, 0),  # Yellow
}

# =====================
# --- BUTTON SETUP ---
# =====================
Bluebutton = Pin(12, Pin.IN, Pin.PULL_UP)
Whitebutton = Pin(13, Pin.IN, Pin.PULL_UP)
Redbutton = Pin(14, Pin.IN, Pin.PULL_UP)
Yellowbutton = Pin(15, Pin.IN, Pin.PULL_UP)

# =====================
# --- CODE SETUP ---
# =====================
CORRECT_CODE = ["B", "W", "R", "Y"]  # You can change this sequence
entered_code = []


# =====================
# --- HELPER FUNCTIONS ---
# =====================
def light_led(color):
    """Light up one LED in its color briefly."""
    np.fill((0, 0, 0))  # turn all off first
    if color == "B":
        np[0] = LED_COLORS["B"]
    elif color == "W":
        np[1] = LED_COLORS["W"]
    elif color == "R":
        np[2] = LED_COLORS["R"]
    elif color == "Y":
        np[3] = LED_COLORS["Y"]
    np.write()
    sleep(0.5)
    np.fill((0, 0, 0))  # turn off
    np.write()


def check_code():
    """Check entered code against CORRECT_CODE."""
    global entered_code
    if entered_code == CORRECT_CODE:
        lcd.clear()
        lcd.putstr("Correct!")
        RotateCW(100)
        sleep(2)
        StopMotor()
        lcd.clear()
        lcd.putstr("Press Blue")
        lcd.move_to(0, 1)
        lcd.putstr("button to close")
        while True:
            if Bluebutton.value() == 0:
                light_led("B")
                # close motor
                RotateCCW(100)
                sleep(2)
                StopMotor()
                break
            sleep(0.3)

    else:
        lcd.clear()
        lcd.putstr("Incorrect!")
    sleep(2)
    lcd.clear()
    lcd.putstr("Enter Code:")
    entered_code = []


# =====================
# --- MAIN LOOP ---
# =====================
while True:
    if Bluebutton.value() == 0:
        print("Blue Button Pressed")
        light_led("B")
        entered_code.append("B")
        lcd.putstr("*")
        sleep(0.3)

    if Whitebutton.value() == 0:
        print("White Button Pressed")
        light_led("W")
        entered_code.append("W")
        lcd.putstr("*")
        sleep(0.3)

    if Redbutton.value() == 0:
        print("Red Button Pressed")
        light_led("R")
        entered_code.append("R")
        lcd.putstr("*")
        sleep(0.3)

    if Yellowbutton.value() == 0:
        print("Yellow Button Pressed")
        light_led("Y")
        entered_code.append("Y")
        lcd.putstr("*")
        sleep(0.3)

    # Once 4 buttons are pressed, check code
    if len(entered_code) == 4:
        check_code()
