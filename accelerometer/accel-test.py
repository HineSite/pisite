import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

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


    if deltaz > tolerance or deltay > tolerance or deltax > tolerance:
        changed = True

    if changed:
        print(' delta (Z: {z}, X: {x}, Y: {y})'.format(z = deltaz, x = deltax, y = deltay))
        print('actual (Z: {z}, X: {x}, Y: {y})'.format(z = valz, x = valx, y = valy))
        print(' baseD (Z: {z}, X: {x}, Y: {y})'.format(z = baseDz, x = baseDx, y = baseDy))
        print('')

        lastz = valz
        lasty = valy
        lastx = valx

    time.sleep(0.01)
