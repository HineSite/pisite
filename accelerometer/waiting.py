import time
import busio
import digitalio
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import board
import neopixel

# pixel setup
PIXEL_PIN = board.D18
NUM_PIXELS = 50
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=.1, auto_write=True, pixel_order=ORDER)
CLEAR = (0, 0, 0)

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)


def map(value, from_min, from_max, to_min, to_max):
    # this remaps a value from original range to new range
    left_span = from_max - from_min
    right_span = to_max - to_min

    # Convert the left range into a 0-1 range (int)
    valueScaled = int(value - from_min) / int(left_span)

    # Convert the 0-1 range into a value in the right range.
    return int(to_min + (valueScaled * right_span))


chanz = AnalogIn(mcp, MCP.P0)
chany = AnalogIn(mcp, MCP.P1)
chanx = AnalogIn(mcp, MCP.P2)

lastz = chanz.value
lasty = chany.value
lastx = chanx.value

tolerance = 1000
color = (0, 0, 0)
timeout = 1

while True:
    valz = chanz.value
    valy = chany.value
    valx = chanx.value

    deltaz = abs(valz - lastz)
    deltay = abs(valy - lasty)
    deltax = abs(valx - lastx)

    mapz = map(valz, 0, 65535, 0, 255)
    mapy = map(valy, 0, 65535, 0, 255)
    mapx = map(valx, 0, 65535, 0, 255)

    if deltaz > tolerance or deltay > tolerance or deltax > tolerance:
        timeout = 1
        lastz = valz
        lasty = valy
        lastx = valx
        color = (mapz, mapy, mapx)
        pixels[24] = color
    elif timeout > 0:
        timeout = timeout - .05
        if timeout < 0:
            timeout = 0
        temp = (int(max(color[0] * timeout, 0)), int(max(color[1] * timeout, 0)), int(max(color[2] * timeout, 0)))
        pixels[24] = temp

    time.sleep(0.1)
