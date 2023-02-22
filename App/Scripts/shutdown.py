# Flashes the light red 3 times. Intended as a precursor to shutting down or restarting.

import time
import board
import RPi.GPIO as GPIO
import neopixel

# Configure the setup
PIXEL_PIN = board.D18  # pin that the NeoPixel is connected to
NUM_PIXELS = 50
ORDER = neopixel.RGB
CLEAR = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)

# Create the NeoPixel object
pixels = neopixel.NeoPixel(
  PIXEL_PIN, NUM_PIXELS, brightness=.1, auto_write=False, pixel_order=ORDER
)


pixels.fill(RED)
pixels.show()
time.sleep(.1)

pixels.fill(CLEAR)
pixels.show()
time.sleep(.1)

pixels.fill(RED)
pixels.show()
time.sleep(.1)

pixels.fill(CLEAR)
pixels.show()
time.sleep(.1)

pixels.fill(RED)
pixels.show()
time.sleep(.1)

pixels.fill(CLEAR)
pixels.show()
