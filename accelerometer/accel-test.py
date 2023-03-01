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

resolution = 16
scale_factor = .33
tolerance = 1000
sleep = 0.100

chanx = AnalogIn(mcp, MCP.P2)
chany = AnalogIn(mcp, MCP.P1)
chanz = AnalogIn(mcp, MCP.P0)

initial_x = chanx.value
initial_y = chany.value
initial_z = chanz.value

last_x = initial_x
last_y = initial_y
last_z = initial_z

time.sleep(sleep)


def remap(value, from_min, from_max, to_min, to_max):
    # this remaps a value from original range to new range
    left_span = from_max - from_min
    right_span = to_max - to_min

    # Convert the left range into a 0-1 range (int)
    scaled_value = int(value - from_min) / int(left_span)

    # Convert the 0-1 range into a value in the right range.
    return int(to_min + (scaled_value * right_span))
#remap


first = True
while True:
    changed = False

    current_x = chanx.value
    current_y = chany.value
    current_z = chanz.value

    delta_x = abs(current_x - last_x)
    delta_y = abs(current_y - last_y)
    delta_z = abs(current_z - last_z)

    initial_delta_x = abs(initial_x - current_x)
    initial_delta_y = abs(initial_y - current_y)
    initial_delta_z = abs(initial_z - current_z)

    # Caculate 360deg values like so: atan2(-yAng, -zAng)
    # atan2 outputs the value of -π to π (radians)
    # We are then converting the radians to degrees
    remapped_x = remap(current_x, 0, 65535, -90, 90)
    remapped_y = remap(current_y, 0, 65535, -90, 90)
    remapped_z = remap(current_z, 0, 65535, -90, 90)

    angle_x = round(math.degrees(math.atan2(-remapped_y, -remapped_z) + math.pi))
    angle_y = round(math.degrees(math.atan2(-remapped_x, -remapped_z) + math.pi))
    angle_z = round(math.degrees(math.atan2(-remapped_y, -remapped_x) + math.pi))

    if delta_z > tolerance or delta_y > tolerance or delta_x > tolerance:
        changed = True

    if changed or first:
        print('delta (X: {x}, Y: {y}, Z: {z})'.format(x=delta_x, y=delta_y, z=delta_z))
        print('current (X: {x}, Y: {y}, Z: {z})'.format(x=current_x, y=current_y, z=current_z))
        print('initial delta (X: {x}, Y: {y}, Z: {z})'.format(x=initial_delta_x, y=initial_delta_y, z=initial_delta_z))
        print('remapped (X: {x}, Y: {y}, Z: {z})'.format(x=remapped_x, y=remapped_y, z=remapped_z))
        print('angle (X: {x}, Y: {y}, Z: {z})'.format(x=angle_x, y=angle_y, z=angle_z))
        print('')

        last_x = current_x
        last_y = current_y
        last_z = current_z
    #fi

    first = False
    time.sleep(sleep)
#end_while
