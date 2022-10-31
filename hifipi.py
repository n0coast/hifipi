from PIL import Image, ImageDraw, ImageFont
from ST7789 import ST7789
import os
import subprocess
# imports for buttons
import signal
import RPi.GPIO as GPIO
import time

# =======================================================
# Set up the screen and image buffers
# =======================================================
# Set up screen
SPI_SPEED_MHZ = 80
screen = ST7789(
    rotation=90,  # Needed to display the right way up on Pirate Audio
    port=0,  # SPI port
    cs=1,  # SPI port Chip-select channel
    dc=9,  # BCM pin used for data/command
    backlight=13,
    spi_speed_hz=SPI_SPEED_MHZ * 1000 * 1000
)
# screen size details
width = screen.width
height = screen.height

# Create a few blank images.
# This lets us set up layouts/pictures, then send them easily to the acreen
# We set up an array of images and a corresponding array of draw objects, one for each image
image = [Image.new("RGB", (240, 240), (0, 0, 0)) for i in range(4)]
draw = [ImageDraw.Draw(image[i]) for i in range(4)]

# =======================================================
# Set up a font to use when showing text
# =======================================================
# I've shown how to create two different sizes
# You need a font file in the appropriate directory.
# If using Raspbian lite, you'll need to create the directory and get a font from (eg) https://www.fontsquirrel.com/
font30 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
font60 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)

# =======================================================
# Define how to run 'mpg123', and some radio station streaming urls
# =======================================================
mpg123_command = 'mpg123 -q'
kexp_stream_url = 'http://kexp-mp3-128.streamguys1.com/kexp128.mp3'
kuow_stream_url = 'http://playerservices.streamtheworld.com/api/livestream-redirect/KUOWFM_HIGH_MP3.mp3'
kexp_command = f'{mpg123_command} {kexp_stream_url}'
kuow_command = f'{mpg123_command} {kuow_stream_url}'

# =======================================================
# Define how to run 'spotfiyd'
# =======================================================
spotifyd_command = f'./spotifyd --no-daemon --bitrate 320 --device-name hifipi'

# =======================================================
# Set up the basics for buttons
# =======================================================
# The buttons on Pirate Audio are connected to pins 5, 6, 16 and 20
BUTTONS = [5, 6, 16, 24]

# These correspond to buttons A, B, X and Y respectively
LABELS = ['A', 'B', 'X', 'Y']

# Set up RPi.GPIO with the "BCM" numbering scheme
GPIO.setmode(GPIO.BCM)

# Buttons connect to ground when pressed, so we should set them up
# with a "PULL UP", which weakly pulls the input signal to 3.3V.
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# NB: Further down, we'll set up the button handler which will tell teh pi what to do on each button pressed

# ================================END OF THE BASIC SETUP======================

# =======================================================
# Set up our actual images
# =======================================================
# image 0 should already be a black screen as that's how we set them all up.  It's useful when we end the program
# image 1: get pi logo.  raspberrypi.png should be a 240x240 image in the same directory as the program
# image[1] = Image.open("raspberrypi.png")

# image 2: draw a multicoloured series of small boxes over the display.
# This uses the 'draw' object associated with image3
# draw.rectangle ((x0,y0,x1,y1),(r,g,b)) draws a box from x1,y1 to x2,y2, using r,g,b as colour values
# for row in range(10):
#     for cell in range(10):
#         draw[2].rectangle((cell * 24, row * 24, cell * 24 + 24, row * 24 + 24), (cell * 25, row * 25, 0))


# image 3 uses drawing text to put a menu item next to each button
# let's have a function to do the repettitive stuff
def show_text(draw, message, x, y, font, ralign):
    size_x, size_y = draw.textsize(message, font)
    text_y = y - size_y
    text_x = x
    if ralign:
        text_x = x - size_x
    draw.text((text_x, text_y), message, font=font, fill=(255, 255, 255))


show_text(draw[3], "KEXP", 0, 90, font30, False)
show_text(draw[3], "KUOW", 0, 200, font30, False)
show_text(draw[3], "Spotify", 240, 90, font30, True)
show_text(draw[3], "Stop", 240, 200, font30, True)

#global process


def run_command(command):
    global process
    try:
        if command.split() == process.args:
            return
    except NameError:
        pass
    try:
        process.terminate()
    except NameError:
        pass

    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

# =======================================================
# Set up the button handler
# =======================================================
def handle_button(pin):
    label = LABELS[BUTTONS.index(pin)]
    # print("Button press detected on pin: {} label: {}".format(pin, label))

    if label == 'A':
        screen.display(image[0])
        run_command(kexp_command)
        screen.display(image[3])

    if label == 'B':
        screen.display(image[0])
        run_command(kuow_command)
        screen.display(image[3])

    if label == 'X':
        screen.display(image[0])
        run_command(spotifyd_command)
        screen.display(image[3])

    if label == 'Y':
        screen.display(image[0])
        process.terminate()
        screen.display(image[3])


# Loop through out buttons and attach the "handle_button" function to each
# We're watching the "FALLING" edge (transition from 3.3V to Ground) and
# picking a generous bouncetime of 300ms to smooth out button presses.
for pin in BUTTONS:
    GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=300)

# Now that we are all set up, show the menu screen (image 3)
screen.display(image[3])

# Finally, since button handlers don't require a "while True" loop,
# we pause the script to prevent it exiting immediately.
signal.pause()


GPIO.cleanup()
exit()
