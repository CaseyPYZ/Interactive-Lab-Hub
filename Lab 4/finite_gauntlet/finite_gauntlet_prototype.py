# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2017 James DeVito for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!

import time
import subprocess
import t9_imitation as t9

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

# Speak
def speak(instruction):
    command = """
        say() { 
            local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; 
        } ; 
    """ + f"say '{instruction}'"
    subprocess.call(command, shell=True)

# Get gesture from APDS9960
def get_gesture():
    gesture = apds.gesture()
    if gesture == 0x03:
        return "LEFT"
    elif gesture == 0x04:
        return "RIGHT"

    return False

# Input buffers
NUM_LST = [] # global
WORD_LST = []
TEMP_WORD = ""
SENTENCE = []

# Cap values: 8/9/10/11
def get_t9_input(TEMP_WORD, WORD_LST, SENTENCE):    
    
    # Capacitive sensor values
    caps = [False] * 4
    
    # Check capacitive sensor values
    for i in range(4):
        if mpr121[ i + 8 ].value:
            caps[i] = True
    
    if caps[0] and caps[1] and caps[2] and caps[3]:
        # space: push current word to SENTENCE & clear NUM_LST
        if len(WORD_LST) > 0:
            SENTENCE.append(WORD_LST[0])
        else:
            SENTENCE.append(TEMP_WORD)
        NUM_LST.clear()
    elif caps[1] and caps[2] and caps[3]: 
        # 1: '
        NUM_LST.append(1)
    elif caps[0] and caps[1] and caps[2]: 
        # 9
        NUM_LST.append(9)
    elif caps[2] and caps[3]: 
        # 8
        NUM_LST.append(8)
    elif caps[1] and caps[2]: 
        # 7
        NUM_LST.append(7)
    elif caps[0] and caps[1]: 
        # 6
        NUM_LST.append(6)
    elif caps[3]:
        # 5
        NUM_LST.append(5)
    elif caps[2]:
        # 4
        NUM_LST.append(4)
    elif caps[1]:
        # 3
        NUM_LST.append(3)
    elif caps[0]:
        # 2
        NUM_LST.append(2)

    # Get current word list
    if len(NUM_LST) > 0:
        WORD_LST = t9.try_it(NUM_LST)
        if len(WORD_LST) > 0:
            TEMP_WORD = WORD_LST[0][:len(NUM_LST)]
            print("NUM LST> ", NUM_LST, "TEMP_WORD>", TEMP_WORD, "WORD LST> ", WORD_LST)
        else:
            print("NUM LST> ", NUM_LST, " No possible word")

    return TEMP_WORD, WORD_LST, SENTENCE


while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Check capacitive sensor values
    TEMP_WORD, WORD_LST, SENTENCE = get_t9_input(TEMP_WORD, WORD_LST, SENTENCE)

    # Display text on OLED screen
    draw.text((x, top + 0), TEMP_WORD, font=font, fill=255)
    draw.text((x, top + 10), ', '.join(WORD_LST), font=font, fill=255)
    draw.text((x, top + 20), ' '.join(SENTENCE), font=font, fill=255)

    # Speak if SENTENCE & RIGHT
    if len(SENTENCE) > 0:
        # Get gesture
        GESTURE = get_gesture()
        # print(GESTURE)
        if GESTURE and GESTURE == "RIGHT":
            # Speak
            speak(' '.join(SENTENCE))
            # Clear input buffer
            TEMP_WORD = ""
            SENTENCE.clear()

    # Backspace
    if len(TEMP_WORD) > 0:
        GESTURE = get_gesture()
        print(GESTURE)
        if GESTURE and GESTURE == "LEFT":
            print("backspace")
            NUM_LST.pop(-1)

    # Display image.
    disp.image(image)
    disp.show()
    time.sleep(0.5)