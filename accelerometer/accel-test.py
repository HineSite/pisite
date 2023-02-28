import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import math

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)


chanx = AnalogIn(mcp, MCP.P2)
chany = AnalogIn(mcp, MCP.P1)
chanz = AnalogIn(mcp, MCP.P0)

basex = chanx.value
basey = chany.value
basez = chanz.value

lastx = basex
lasty = basey
lastz = basez

tolerance = 1000


def remap(value, from_min, from_max, to_min, to_max):
    # this remaps a value from original range to new range
    left_span = from_max - from_min
    right_span = to_max - to_min

    # Convert the left range into a 0-1 range (int)
    scaled_value = int(value - from_min) / int(left_span)

    # Convert the 0-1 range into a value in the right range.
    return int(to_min + (scaled_value * right_span))


first = True
while True:
    changed = False

    valx = chanx.value
    valy = chany.value
    valz = chanz.value

    deltax = abs(valx - lastx)
    deltay = abs(valy - lasty)
    deltaz = abs(valz - lastz)

    baseDx = abs(basex - valx)
    baseDy = abs(basey - valy)
    baseDz = abs(basez - valz)

    # Caculate 360deg values like so: atan2(-yAng, -zAng)
    # atan2 outputs the value of -π to π (radians)
    # We are then converting the radians to degrees
    mapx = remap(valx, 0, 65535, -90, 90)
    mapy = remap(valy, 0, 65535, -90, 90)
    mapz = remap(valz, 0, 65535, -90, 90)

    angx = math.degrees(math.atan2(-mapy, -mapz) + math.pi)
    angy = math.degrees(math.atan2(-mapx, -mapz) + math.pi)
    angz = math.degrees(math.atan2(-mapy, -mapx) + math.pi)

    if deltaz > tolerance or deltay > tolerance or deltax > tolerance:
        changed = True

    if changed or first:
        print('delta (X: {x}, Y: {y}, Z: {z})'.format(x=deltax, y=deltay, z=deltaz))
        print('actual (X: {x}, Y: {y}, Z: {z})'.format(x=valx, y=valy, z=valz))
        print('baseD (X: {x}, Y: {y}, Z: {z})'.format(x=baseDx, y=baseDy, z=baseDz))
        print('mapped (X: {x}, Y: {y}, Z: {z})'.format(x=mapx, y=mapy, z=mapz))
        print('angle (X: {x}, Y: {y}, Z: {z})'.format(x=angx, y=angy, z=angz))
        print('')

        lastx = valx
        lasty = valy
        lastz = valz

    first = False

    time.sleep(0.01)
