import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import math
import board
import RPi.GPIO as GPIO
import signal
import sys

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

resolution = 65535  # (2 ^ 16 - 1)
tolerance = 1000
sleep = 0.100

chanx = AnalogIn(mcp, MCP.P2)
chany = AnalogIn(mcp, MCP.P1)
chanz = AnalogIn(mcp, MCP.P0)


def get_value(channel):
    # This just needs to shift the value by half to get a range from -32767.5 to 32767.5
    return channel.value - (resolution * .5)
# get_value


def remap(value, to_min, to_max):
    res = (resolution * .5)
    from_min = -res
    from_max = res

    # this remaps a value from original range to new range
    left_span = from_max - from_min
    right_span = to_max - to_min

    # Convert the left range into a 0-1 range (int)
    scaled_value = int(value - from_min) / int(left_span)

    # Convert the 0-1 range into a value in the right range.
    return int(to_min + (scaled_value * right_span))
# remap


def handle_signal(sig, frame):
    GPIO.cleanup()
    sys.exit(0)
# handle_signal


def on_button_pressed(channel):
    print_readings()
# on_button_pressed


initial_x = None
initial_y = None
initial_z = None

last_x = None
last_y = None
last_z = None


def print_readings():
    global initial_x
    global initial_y
    global initial_z

    global last_x
    global last_y
    global last_z

    current_x = get_value(chanx)
    current_y = get_value(chany)
    current_z = get_value(chanz)

    if initial_x is None:
        print("Initial Readings:")
        initial_x = current_x
        initial_y = current_y
        initial_z = current_z

        last_x = current_x
        last_y = current_y
        last_z = current_z
    # fi

    delta_x = abs(current_x - last_x)
    delta_y = abs(current_y - last_y)
    delta_z = abs(current_z - last_z)

    initial_delta_x = abs(initial_x - current_x)
    initial_delta_y = abs(initial_y - current_y)
    initial_delta_z = abs(initial_z - current_z)

    g_x = (current_x / (resolution * .1))
    g_y = (current_y / (resolution * .1))
    g_z = (current_z / (resolution * .1))

    # Calculate 360deg values like so: atan2(-yAng, -zAng)
    # atan2 outputs the value of -π to π (radians)
    # We are then converting the radians to degrees
    remapped_x = remap(current_x, -90, 90)
    remapped_y = remap(current_y, -90, 90)
    remapped_z = remap(current_z, -90, 90)

    angle_x = round(math.degrees(math.atan(g_y / g_z)))
    angle_y = round(math.degrees(math.atan(g_x / g_z)))
    angle_z = round(math.degrees(math.atan(g_y / g_x)))

    print('current (X: {x}, Y: {y}, Z: {z})'.format(x=current_x, y=current_y, z=current_z))
    print('g-force (X: {x}, Y: {y}, Z: {z})'.format(x=g_x, y=g_y, z=g_z))
    print('delta (X: {x}, Y: {y}, Z: {z})'.format(x=delta_x, y=delta_y, z=delta_z))
    print('initial delta (X: {x}, Y: {y}, Z: {z})'.format(x=initial_delta_x, y=initial_delta_y, z=initial_delta_z))
    print('remapped (X: {x}, Y: {y}, Z: {z})'.format(x=remapped_x, y=remapped_y, z=remapped_z))
    print('angle (X: {x}, Y: {y}, Z: {z})'.format(x=angle_x, y=angle_y, z=angle_z)) # -y: Tilted to Left | +y: Titled to Right | -x: Tilted Twards User | +x: Tilted away from User
    print('')

    last_x = current_x
    last_y = current_y
    last_z = current_z
# print_readings


# Get and print initial readings
print_readings()


# Button setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(17, GPIO.FALLING, callback=on_button_pressed, bouncetime=250)

signal.signal(signal.SIGINT, handle_signal)
signal.pause()

GPIO.cleanup()
