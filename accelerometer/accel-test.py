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


chanz = AnalogIn(mcp, MCP.P0)
chany = AnalogIn(mcp, MCP.P1)
chanx = AnalogIn(mcp, MCP.P2)

basez = chanz.value
basey = chany.value
basex = chanx.value

lastz = basez
lasty = basey
lastx = basex

tolerance = 750

print('base (Z: {z}, X: {x}, Y: {y})'.format(z = basez, x = basex, y = basey))

def map(value, from_min, from_max, to_min, to_max):
    # this remaps a value from original range to new range
    left_span = from_max - from_min
    right_span = to_max - to_min

    # Convert the left range into a 0-1 range (int)
    valueScaled = int(value - from_min) / int(left_span)

    # Convert the 0-1 range into a value in the right range.
    return int(to_min + (valueScaled * right_span))


first = True
while True:
    changed = False

    valz = chanz.value
    valy = chany.value
    valx = chanx.value

    deltaz = abs(valz - lastz)
    deltay = abs(valy - lasty)
    deltax = abs(valx - lastx)

    baseDz = abs(basez - valz)
    baseDy = abs(basey - valy)
    baseDx = abs(basex - valx)

    # Caculate 360deg values like so: atan2(-yAng, -zAng)
    # atan2 outputs the value of -π to π (radians)
    # We are then converting the radians to degrees
    mapz = map(valz, 0, 65535, -90, 90)
    mapy = map(valy, 0, 65535, -90, 90)
    mapx = map(valx, 0, 65535, -90, 90)

    angz = math.degrees(math.atan2(-mapy, -mapx) + math.pi)
    angy = math.degrees(math.atan2(-mapx, -mapz) + math.pi)
    angx = math.degrees(math.atan2(-mapy, -mapz) + math.pi)

    if deltaz > tolerance or deltay > tolerance or deltax > tolerance:
        changed = True

    if changed or first:
        print(' delta (Z: {z}, X: {x}, Y: {y})'.format(z = deltaz, x = deltax, y = deltay))
        print('actual (Z: {z}, X: {x}, Y: {y})'.format(z = valz, x = valx, y = valy))
        print(' baseD (Z: {z}, X: {x}, Y: {y})'.format(z = baseDz, x = baseDx, y = baseDy))
        print('mapped (Z: {z}, X: {x}, Y: {y})'.format(z = mapz, x = mapy, y = mapx))
        print(' angle (Z: {z}, X: {x}, Y: {y})'.format(z = angz, x = angy, y = angx))
        print('')

        lastz = valz
        lasty = valy
        lastx = valx

    first = False

    time.sleep(0.01)
