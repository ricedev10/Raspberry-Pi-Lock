# About

Pico code for pico microcontroller project. This is essentially for a coded padlock that opens a drawer.

# Goal

1. To create a 4-digit padlock keycode
2. When pressing one of 4 buttons, a corresponding LED lights up to indicate it was pressed
3. LCD Display (for display "Incorrect/Correct" and other information)
4. After pressing 4 digits, program automatically detects if inputted keycode is correct or not
5. LCD display will show:
   a. Incorrect: Enter keycode again
   b. Correct: Automatically opens drawer and gives options to press button A for changing keycode (see [Setting & Resetting the Pin](#setting-&-resetting-the-pin) below) & button B for closing drawer

# Setting & Resetting the Pin

1. After entering the correct pin, the drawer opens and the following occurs:
2. LCD Display gives option to press button A for closing drawer (This will "reset" the circuit - must enter keycode again) OR...
3. LCD Display gives option to press button B for changing keycode this will start the process of changing the keycode. Once B is pressed, you enter 4 digits, and to confirm you press button B once more. You can now close drawer or reset code again (goes back to step 1).
