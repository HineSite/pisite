import time
import board
import RPi.GPIO as GPIO
import neopixel
import sys
import signal

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # Use physical pin numbering
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Configure the setup
PIXEL_PIN = board.D18  # pin that the NeoPixel is connected to
NUM_PIXELS = 50
ORDER = neopixel.RGB

# Create the NeoPixel object
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=1, auto_write=True, pixel_order=ORDER)

BTN_STATE = 0


def handle_signal(sig, frame):
    GPIO.cleanup()
    sys.exit(0)


def setbtn(state):
    global BTN_STATE
    BTN_STATE = state


signal.signal(signal.SIGINT, handle_signal)

while True:
    # if the button is not pressed
    if GPIO.input(23):
        setbtn(0)
    else:
        if BTN_STATE is 0:
            setbtn(1)
            pixels.fill((0, 255, 0))
            time.sleep(.1)
            pixels.fill((0, 0, 0))
            exec(open("/var/www/html/App/Scripts/button.py").read())
    time.sleep(.1)
