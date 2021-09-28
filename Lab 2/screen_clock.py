import datetime
import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from adafruit_rgb_display.rgb import color565
import random

from dot import Dot

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# CLOCK_COLOR = "#00C4AA"
DOT_SIZE = 4

X_SLOTS = 60

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

# Buttons
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

def get_org_coord():
    org_x0 = (counter % X_SLOTS) + (DOT_SIZE * (counter % X_SLOTS))
    org_y0 = (counter // X_SLOTS) + (DOT_SIZE * (counter // X_SLOTS))
    org_x1 = org_x0 + DOT_SIZE
    org_y1 = org_y0 + DOT_SIZE
    print('org_coord', org_x0, org_y0, org_x1, org_y1)
    return [org_x0, org_y0, org_x1, org_y1]
    # return [org_y0, org_x0, org_y1, org_x1]


# Setup
draw.rectangle((0, 0, width, height), outline=0, fill=0)


# Initiate global counter & dots list
counter = 0
dots = []


# Time passed today before clock activated
now = datetime.datetime.now(tz=None)
midnight = now.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
last_minute = now
seconds = (now - midnight).seconds

# for s in range(seconds):
#     draw.ellipse(get_random_ellipse_coord(), fill=CLOCK_COLOR, outline=None)


for s in range(seconds):
    if s % 60 == 0:
        #draw.ellipse(get_random_ellipse_coord(), fill=get_ellipse_color(), outline=None)
        new_dot = Dot(draw, (width, height), DOT_SIZE, get_org_coord())
        dots.append(new_dot)
        counter += 1


while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    #TODO: Lab 2 part D work should be filled in here. You should be able to look in cli_clock.py and stats.py 
    ### Barebones Clock
    #TIME = time.strftime("%m/%d/%Y %H:%M:%S")
    # TIME = str(seconds)
    # y = top
    # draw.text((x,y), TIME, font=font, fill="#FFFFFF")
    ### End of Part D

    # Make new dot for every new minute
    now = datetime.datetime.now(tz=None)
    if (now - last_minute).seconds % 60 == 0:
        new_dot = Dot(draw, (width, height), DOT_SIZE, get_org_coord())
        dots.append(new_dot)
        counter += 1
        print(counter)
        last_minute = now
        time.sleep(1)

    # If Button A is pressed
    if not buttonA.value and buttonB.value:
        for d in dots:
            d.go_org()
    
    if not buttonB.value and buttonA.value:
        for d in dots:
            d.go_rand()

    # Draw dots
    for d in dots:
        d.show()

    # Display image.
    disp.image(image, rotation)
