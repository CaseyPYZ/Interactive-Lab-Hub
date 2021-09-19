import datetime
import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import random

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

CLOCK_COLOR = "#00C4AA"

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

def get_random_ellipse_coord():
    # x0 = round(random.uniform(3, width - 3.2), 1)
    # y0 = round(random.uniform(3, height - 3.2), 1)
    x0 = random.randint(0, width - 1)
    y0 = random.randint(0, height - 1)
    x1 = x0 + 1
    y1 = y0 + 1
    print(x0, y0, x1, y1)
    return [x0, y0, x1, y1]


# Setup
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Time passed in today before clock activated
now = datetime.datetime.now(tz=None)
midnight = now.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
seconds = (now - midnight).seconds

# for s in range(seconds):
#     draw.ellipse(get_random_ellipse_coord(), fill=CLOCK_COLOR, outline=None)

counter = 0

while True:
    # Draw a black filled box to clear the image.
    #draw.rectangle((0, 0, width, height), outline=0, fill=0)

    #TODO: Lab 2 part D work should be filled in here. You should be able to look in cli_clock.py and stats.py 
    ### Barebones Clock
    #TIME = time.strftime("%m/%d/%Y %H:%M:%S")
    # TIME = str(seconds)
    # y = top
    # draw.text((x,y), TIME, font=font, fill="#FFFFFF")
    ### End of Part D


    draw.ellipse(get_random_ellipse_coord(), fill=CLOCK_COLOR, outline=None)

    print(counter)
    counter+=1
    
    # Display image.
    disp.image(image, rotation)
    time.sleep(1)
