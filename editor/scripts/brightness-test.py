import time
import board
import RPi.GPIO as GPIO
import neopixel

# pixel setup
PIXEL_PIN = board.D18
NUM_PIXELS = 50
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=1, auto_write=True, pixel_order=ORDER)

CLEAR = (0, 0, 0)
COLOR = (172, 185, 175)

i = 1
while i > 0:
    pixels[24] = (COLOR[0] * i, COLOR[1] * i, COLOR[2] * i)
    i = i - .013
    time.sleep(.013)

pixels[24] = CLEAR
