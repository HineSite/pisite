import sys
import board
import RPi.GPIO as GPIO
import neopixel
import json

# Configure the setup
PIXEL_PIN = board.D18  # pin that the NeoPixel is connected to
NUM_PIXELS = 50
ORDER = neopixel.RGB

# it should always have at least 3
# 1) the name of the script
# 2) the command
# 3) any additional arguments needed by the command
if len(sys.argv) < 3:
    print("invalid args: ", sys.argv)
    sys.exit(420)

if sys.argv[1] == "write":
    color = (int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))

    pixels = neopixel.NeoPixel(
        PIXEL_PIN, NUM_PIXELS, brightness=.1, auto_write=True, pixel_order=ORDER
    )

    if sys.argv[2].isnumeric() and 0 <= int(sys.argv[2]) < NUM_PIXELS:
        pixels[int(sys.argv[2])] = color
    elif sys.argv[2] == "all":
        pixels.fill(color)
elif sys.argv[1] == "update":
    pixels = neopixel.NeoPixel(
        PIXEL_PIN, NUM_PIXELS, brightness=.1, auto_write=False, pixel_order=ORDER
    )

    leds = json.loads(sys.argv[2])
    for led in leds:
        pixels[led['id']] = led['color']

    pixels.show()
