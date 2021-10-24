# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2017 James DeVito for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!

import time
import subprocess

from PIL import Image, ImageDraw, ImageFont

from board import SCL, SDA
import busio

import adafruit_ssd1306
import adafruit_mpr121
from adafruit_apds9960.apds9960 import APDS9960

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create MPR121 capacitive sensor class
mpr121 = adafruit_mpr121.MPR121(i2c)

# Create the proximity sensor class
apds = APDS9960(i2c)
apds.enable_proximity = True
apds.enable_gesture = True

# Create the SSD1306 OLED class.
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

# Get gesture from APDS9960
def get_gesture():
    gesture = apds.gesture()

    if gesture == 0x03:
        return "LEFT"
    elif gesture == 0x04:
        return "RIGHT"

    return False

# Get 9-key input from capacitive sensor values
def get_9key_input():
    


while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Text for display
    CAP_TOUCHED = -1

    # Check capacitive sensor values
    for i in range(12):
        if mpr121[i].value:
            CAP_TOUCHED = i

    # Display text on OLED screen
    if CAP_TOUCHED != -1:
        draw.text((x, top + 8), "CAP> " + str(CAP_TOUCHED) + " touched!", font=font, fill=255)

    # Get gesture
    GESTURE = get_gesture()
    if GESTURE:
        print(GESTURE)
        draw.text((x, top + 16), "GEST> " + GESTURE + " !", font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.show()
    time.sleep(0.1)