import time
import board
import RPi.GPIO as GPIO
import neopixel

pixels = None

def setupLeds():
  global pixels

  # You should not modify anything in here...
  PIXEL_PIN = board.D18
  NUM_PIXELS = 50
  ORDER = neopixel.RGB

  pixels = neopixel.NeoPixel(
    PIXEL_PIN, NUM_PIXELS, brightness=.1, auto_write=True, pixel_order=ORDER
  )
#end
setupLeds()


# ------------------------------ Setup
COLORA = (0, 0, 0)
COLORB = (172, 185, 175)


for i in range(0, 3):
  pixels.fill(COLORB)
  time.sleep(.3)
  pixels.fill(COLORA)
  time.sleep(.3)

pixels.fill((0, 0, 0))
