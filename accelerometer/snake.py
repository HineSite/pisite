import os
import time
import busio
import digitalio
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import math
import board
import RPi.GPIO as GPIO
import neopixel
from enum import Enum
from copy import copy
import random

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

resolution = 65535  # (2 ^ 16 - 1)
chanx = AnalogIn(mcp, MCP.P2)
chany = AnalogIn(mcp, MCP.P1)
chanz = AnalogIn(mcp, MCP.P0)

high_scores_file = './high-score-snake.txt'
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


class Segment:
    x = 0
    y = 0
    color = (0, 0, 0)

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
    # end_init

    def __copy__(self):
        return type(self)(self.x, self.y, self.color)
    # end_copy
# end_segment


class Direction(Enum):
    NONE = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
# end_direction


def get_value(channel):
    # This just needs to shift the value by half to get a range from -32767.5 to 32767.5
    return channel.value - (resolution * .5)
# get_value


_segment_color = (44, 82, 18)
_head_color = (0, 145, 0)
_red = (255, 0, 0)
_yellow = (155, 155, 0)
_green = (0, 255, 0)
_clear = (0, 0, 0)
_direction = Direction.NONE
_angle_thresh = 0
_update_speed = 0
_apples_per_level = 0
_total_apples = 0

_segments = []
_leds = (
    (6, 7, 20, 21, 34, 35, 48),
    (5, 8, 19, 22, 33, 36, 47),
    (4, 9, 18, 23, 32, 37, 46),
    (3, 10, 17, 24, 31, 38, 45),
    (2, 11, 16, 25, 30, 39, 44),
    (1, 12, 15, 26, 29, 40, 43),
    (0, 13, 14, 27, 28, 41, 42)
)
_segments.append(Segment(3, 3, _head_color))
_apple = ()
_apples = 0

_numbers = (
    ((1, 1), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 5), (2, 5), (2, 4), (2, 3), (2, 2), (2, 1)),
    ((2, 1), (2, 2), (2, 3), (2, 4), (2, 5)),
    ((0, 1), (1, 1), (2, 1), (2, 2), (2, 3), (1, 3), (0, 3), (0, 4), (0, 5), (1, 5), (2, 5)),
    ((0, 1), (1, 1), (2, 1), (2, 2), (2, 3), (1, 3), (0, 3), (2, 4), (2, 5), (1, 5), (0, 5)),
    ((2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (0, 1), (0, 2), (0, 3), (1, 3)),
    ((0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (2, 4), (2, 5), (1, 5), (0, 5), (1, 1), (2, 1)),
    ((2, 1), (1, 1), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 5), (2, 5), (2, 4), (2, 3), (1, 3), (0, 3)),
    ((0, 1), (1, 1), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5)),
    ((0, 1), (1, 1), (2, 1), (2, 2), (2, 3), (1, 3), (0, 4), (0, 5), (1, 5), (2, 5), (2, 4), (0, 3), (0, 2)),
    ((2, 1), (1, 1), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (2, 2), (2, 4), (2, 5), (1, 5), (0, 5))
)


def place_apple():
    global _apple
    collision = True
    x = 3
    y = 3

    # clear the previous apple
    if len(_apple) == 3:
        activate_led(_apple[0], _apple[1], _clear)
    # end_if

    while collision:
        x = random.randint(0, 6)
        y = random.randint(0, 6)
        collision = snake_collides_with(x, y)
    # end_while

    _apple = (x, y, _red)
# place_apple


def activate_led(x, y, color):
    # If the x, y location is within the array
    if x >= 0 and x <= 6 and y >= 0 and y <= 6:
        pixels[_leds[y][x]] = color
    # end_if
# activate_led


def draw_number(number, color):
    if number > 9:
        # 2 digits
        digit1 = number // 10
        digit2 = number % 10

        for led in _numbers[digit1]:
            activate_led(led[0], led[1], color)
        # end_for

        for led in _numbers[digit2]:
            activate_led(led[0] + 4, led[1], color)
        # end_for
    else:
        for led in _numbers[number]:
            activate_led(led[0] + 2, led[1], color)
        # end_for
    # end_if
# draw_number


def show_start_sequence():
    pixels.fill(_clear)

    draw_number(3, _yellow)
    time.sleep(.8)
    pixels.fill(_clear)

    draw_number(2, _yellow)
    time.sleep(.8)
    pixels.fill(_clear)

    draw_number(1, _yellow)
    time.sleep(.8)
    pixels.fill(_clear)

    activate_led(_segments[0].x, _segments[0].y, _segment_color)
# show_start_sequence


def get_high_score():
    if not os.path.exists(high_scores_file):
        return 0
    # end_if

    with open(high_scores_file, 'r') as handle:
        return int(handle.read())
    # end_with
# get_high_score


def save_high_score(new_score):
    if not os.path.exists(high_scores_file):
        os.mknod(high_scores_file)
    # end_if

    with open(high_scores_file, 'r+') as handle:
        handle.truncate()
        handle.write(new_score)
    #end_with
# save_high_score


def show_high_score():
    high_score = get_high_score()
    pixels.fill(_clear)
    draw_number(high_score, _yellow)
    time.sleep(2)
# show_high_score


def show_end_sequence(out_of_bounds):
    if out_of_bounds:
        # The head is off the screen, so we need to make sure all lefs are the segment color
        for segment in _segments:
            activate_led(segment.x, segment.y, _segment_color)
        # end_for

        while len(_segments) > 0:
            segment = _segments.pop(0)
            activate_led(segment.x, segment.y, _clear)

            time.sleep(_update_speed)
        # end_while
    else:
        time.sleep(.5)
    # end_if

    score_color = _red
    high_score = get_high_score()
    if _total_apples > high_score:
        score_color = _green
        save_high_score(_total_apples)
    # end_if

    pixels.fill(_clear)
    draw_number(_total_apples, score_color)
    time.sleep(6)
    pixels.fill(_clear)
# show_end_sequence


def show_level_sequence():
    time.sleep(.8)
    pixels.fill(_clear)
# show_level_sequence


def reset_snake():
    global _direction

    _direction = Direction(random.randint(2, 4))
    _segments.clear()
    _segments.append(Segment(3, 3, _head_color))
# reset_snake


def snake_collides_with(x, y):
    for segment in _segments:
        if segment.x == x and segment.y == y:
            return True
        # end_if
    # end_for

    return False
# snake_collides_with


def reset_board():
    global _apples
    global _direction
    global _angle_thresh
    global _update_speed
    global _apples_per_level
    global _total_apples

    _apples = 0
    _angle_thresh = 5
    _update_speed = .5
    _apples_per_level = 8
    _total_apples = 0

    reset_snake()
# reset_board


show_high_score()
reset_board()
show_start_sequence()
place_apple()

while True:
    g_x = (get_value(chanx) / (resolution * .1))
    g_y = (get_value(chany) / (resolution * .1))
    g_z = (get_value(chanz) / (resolution * .1))

    angle_x = round(math.degrees(math.atan(g_y / g_z)))
    angle_y = round(math.degrees(math.atan(g_x / g_z)))

    # Movement is only allowed on one axis at a time (i.e. diagonal movement is not allowed).
    # Reverse movement is not allowed.
    # Once movement has started, stopping is not allowed.

    if math.fabs(angle_y) > math.fabs(angle_x):
        if angle_y > _angle_thresh and _direction != Direction.LEFT:
            _direction = Direction.RIGHT
        elif angle_y < -_angle_thresh and _direction != Direction.RIGHT:
            _direction = Direction.LEFT
        # end_if
    elif math.fabs(angle_y) < math.fabs(angle_x):
        if angle_x > _angle_thresh and _direction != Direction.DOWN:
            _direction = Direction.UP
        elif angle_x < -_angle_thresh and _direction != Direction.UP:
            _direction = Direction.DOWN
        # end_if
    # end_if

    # Use the last segment as the start location for the next segment
    new_segment = copy(_segments[-1])

    if _direction == Direction.UP:
        new_segment.y -= 1
    elif _direction == Direction.DOWN:
        new_segment.y += 1
    elif _direction == Direction.LEFT:
        new_segment.x -= 1
    elif _direction == Direction.RIGHT:
        new_segment.x += 1
    # end_if

    # If the position of the segment is outside the bounds of the board, then the game is over.
    if new_segment.x < 0 or new_segment.x > 6 or new_segment.y < 0 or new_segment.y > 6:
        show_end_sequence(True)
        break
    # end_if

    # The game is also over if the snake runs into its self
    if snake_collides_with(new_segment.x, new_segment.y):
        show_end_sequence(False)
        break
    # end_if

    _segments[-1].color = _segment_color
    _segments.append(new_segment)

    # Check for apple collision
    new_level = False
    if new_segment.x == _apple[0] and new_segment.y == _apple[1]:
        # Update apple tallies
        # Place a new apple
        # Do not remove snake segment because the snake is now longer.

        _apples += 1
        _total_apples += 1
        _update_speed -= .01

        place_apple()

        if _apples >= _apples_per_level:
            new_level = True
        # end_if
    else:
        # If the snake did not eat an apple, we remove the first segment.
        # This is because we recreate the snake head for every movement.
        # The last segment in the list is always the snakes head, therefore we remove the first segment.
        activate_led(_segments[0].x, _segments[0].y, _clear)
        _segments.pop(0)
    # end_if

    # draw the apple and snake
    if not new_level:
        activate_led(_apple[0], _apple[1], _apple[2])  # Don't draw the apple if going to a new level
    # end_if

    for segment in _segments:
        activate_led(segment.x, segment.y, segment.color)
    # end_for

    if new_level:
        _apples = 0
        _apples_per_level += 3
        pause = True

        show_level_sequence()
        reset_snake()
        show_start_sequence()
        continue
    # end_if

    time.sleep(_update_speed)
# end_while


GPIO.cleanup()
