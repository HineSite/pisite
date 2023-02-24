import time
import board
import RPi.GPIO as GPIO
import neopixel
import signal
import sys


def handle_signal(sig, frame):
    GPIO.cleanup()
    sys.exit(0)


def on_button_pressed(channel):
    pixels.fill((0, 255, 0))
    time.sleep(.2)
    pixels.fill((0, 0, 0))


# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(23, GPIO.FALLING, callback=on_button_pressed, bouncetime=250)

# pixel setup
PIXEL_PIN = board.D18
NUM_PIXELS = 50
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=.1, auto_write=True, pixel_order=ORDER)

signal.signal(signal.SIGINT, handle_signal)
signal.pause()

GPIO.cleanup()
