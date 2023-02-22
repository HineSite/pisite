# Loops through the visible light spectrum one LED at a time.

import time
import board
import neopixel
import random
from threading import Thread

# Configure the setup
PIXEL_PIN = board.D18  # pin that the NeoPixel is connected to
NUM_PIXELS = 50
LAST_PIXEL = 49
ORDER = neopixel.RGB  # pixel color channel order

CLEAR = (0, 0, 0)  # clear
DELAY = .1
fade_on = False
fade_duration = .3
fade_granularity = 20

r = 255
g = 0
b = 0


# Create the NeoPixel object
global pixels
pixels = neopixel.NeoPixel(
  PIXEL_PIN, NUM_PIXELS, brightness=.1, auto_write=False, pixel_order=ORDER
)

class fadeout:
  i = 0
  color = (255, 255, 255)

  def __init__(self, i, color):
    self.i = i
    self.color = color
    self._running = True

  def terminate(self):
    self._running = False

  def run(self):
    global fade_duration
    global fade_granularity

    temp = color
    delay = fade_duration / fade_granularity

    tr = color[0]
    tg = color[1]
    tb = color[2]

    rStep = tr / fade_granularity
    gStep = tg / fade_granularity
    bStep = tb / fade_granularity

    for i in range(fade_granularity):
      tr -= rStep
      if tr < 0:
        tr = 0

      tg -= gStep
      if tg < 0:
        tg = 0

      tb -= bStep
      if tb < 0:
        tb = 0

      pixels[self.i] = (tr, tg, tb)
      pixels.show()
      time.sleep(delay)
#end



def fade(i, color):
#  pixels[i] = CLEAR
#  pixels.show()

  if fade_on:
    fadeoutInst = fadeout(i, color)
    fadeoutThread = Thread(target = fadeoutInst.run)
    fadeoutThread.start()
#end


def getColorRY(i):
  global g
  g += 5
  if g > 255:
    g = 255

  return (r, g, b)
#end


def getColorYG(i):
  global r
  r -= 5
  if r < 0:
    r = 0

  return (r, g, b)
#end


def getColorGB(i):
  global b
  global g

  b += 10
  if b >= 255:
    b = 255

    g -= 10
    if g < 0:
      g = 0

  return (r, g, b)
#end



global last_color
last_color = (r, g, b)

pixels.fill(CLEAR)
pixels.show()






# red to yellow
for i in range(NUM_PIXELS):
  color = getColorRY(i)
  pixels[i] = color
  if i > 0:
    fade(i - 1, last_color)

  last_color = color

  pixels.show()
  time.sleep(DELAY)
#end - 255, 255, 0

fade(LAST_PIXEL, last_color)


# yellow to green
for i in range(NUM_PIXELS):
  color = getColorYG(i)
  pixels[i] = color
  if i > 0:
    fade(i - 1, last_color)

  last_color = color

  pixels.show()
  time.sleep(DELAY)
#end - 0, 255, 0

fade(LAST_PIXEL, last_color)


# green to blue
for i in range(NUM_PIXELS):
  color = getColorGB(i)
  pixels[i] = color
  if i > 0:
    fade(i - 1, last_color)

  last_color = color

  pixels.show()
  time.sleep(DELAY)
#end - 0, 5, 255

fade(LAST_PIXEL, last_color)





time.sleep(.5)
pixels.fill(CLEAR)
pixels.show()
