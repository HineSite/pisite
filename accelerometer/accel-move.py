import os
import time
import busio
import digitalio
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import math
import board
import RPi.GPIO as GPIO
import signal
import sys
import neopixel

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

pixels = None


def setup_leds():
    global pixels

    # You should not modify anything in here...
    PIXEL_PIN = board.D18
    NUM_PIXELS = 50
    ORDER = neopixel.RGB

    pixels = neopixel.NeoPixel(
        PIXEL_PIN, NUM_PIXELS, brightness=.1, auto_write=True, pixel_order=ORDER
    )
# setupLeds


setup_leds()


def get_value(channel):
    # This just needs to shift the value by half to get a range from -32767.5 to 32767.5
    return channel.value - (resolution * .5)


# get_value


def handle_signal(sig, frame):
    pixels.fill((0, 0, 0))
    GPIO.cleanup()
    sys.exit(0)
# handle_signal


initial_x = None
initial_y = None
initial_z = None

last_x = None
last_y = None
last_z = None

signal.signal(signal.SIGINT, handle_signal)

leds = (
    (6, 7, 20, 21, 34, 35, 48),
    (5, 8, 19, 22, 33, 36, 47),
    (4, 9, 18, 23, 32, 37, 46),
    (3, 10, 17, 24, 31, 38, 45),
    (2, 11, 16, 25, 30, 39, 44),
    (1, 12, 15, 26, 29, 40, 43),
    (0, 13, 14, 27, 28, 41, 42)
)
index_y = 3
index_x = 3

led_color = (172, 185, 175)
pixels.fill((0, 0, 0))

pixels[leds[index_y][index_x]] = (255, 0, 0)
time.sleep(2)

pixels[leds[index_y][index_x]] = (255, 255, 0)
time.sleep(2)

pixels[leds[index_y][index_x]] = (0, 255, 0)
time.sleep(2)

pixels[leds[index_y][index_x]] = led_color

while True:
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

    angle_x = round(math.degrees(math.atan(g_y / g_z)))
    angle_y = round(math.degrees(math.atan(g_x / g_z)))
    angle_z = round(math.degrees(math.atan(g_y / g_x)))

    print('current (X: {x}, Y: {y}, Z: {z})'.format(x=current_x, y=current_y, z=current_z))
    print('g-force (X: {x}, Y: {y}, Z: {z})'.format(x=g_x, y=g_y, z=g_z))
    print('delta (X: {x}, Y: {y}, Z: {z})'.format(x=delta_x, y=delta_y, z=delta_z))
    print('initial delta (X: {x}, Y: {y}, Z: {z})'.format(x=initial_delta_x, y=initial_delta_y, z=initial_delta_z))
    print('angle (X: {x}, Y: {y}, Z: {z})'.format(x=angle_x, y=angle_y, z=angle_z))  # -y: Tilted to Left | +y: Titled to Right | -x: Tilted Twards User | +x: Tilted away from User
    print('')

    last_x = current_x
    last_y = current_y
    last_z = current_z

    if angle_y > 10:
        index_x += 1
    # end_if

    if angle_y < -10:
        index_x -= 1
    # end_if

    if index_x < 0:
        index_x = 0
    # end_if

    if index_x > 6:
        index_x = 6
    # end_if



    if angle_x > 10:
        index_y += 1
    # end_if

    if angle_x < -10:
        index_y -= 1
    # end_if

    if index_y < 0:
        index_y = 0
    # end_if

    if index_y > 6:
        index_y = 6
    # end_if

    pixels.fill((0, 0, 0))
    pixels[leds[index_y][index_x]] = led_color

    time.sleep(.2)
# end_while
