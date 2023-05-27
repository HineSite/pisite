import sys

from led_state import LedState
from led import Led
from led_controller import LedController

led_state = LedState()

print('Testing LedState...')

# get pre-initialized led
led = led_state.get_by_id(20)
if led.r != 0 or led.g != 0 or led.b != 0 or led.a != .1:
    print('Pre-initialized failed, got led: {c}'.format(c=led.to_string()))
    sys.exit(1)


# create new led, update the set, then get the led back.
led = Led(20, 102, 0, 102, .3)
led_state.set(led)
led = led_state.get_by_id(20)
if led.r != 102 or led.g != 0 or led.b != 102 or led.a != .3:
    print('Led update failed, got led: {c}'.format(c=led.to_string()))
    sys.exit(1)


# make sure the other colors are still clear
led = led_state.get_by_id(43)
if led.r != 0 or led.g != 0 or led.b != 0 or led.a != .1:
    print('Led update updated too many colors, got led: {c}'.format(c=led.to_string()))
    sys.exit(1)


# clear the colors and recheck
led_state.clear()
led = led_state.get_by_id(20)
if led.r != 0 or led.g != 0 or led.b != 0 or led.a != .1:
    print('Failed to clear colors, got led: {c}'.format(c=led.to_string()))
    sys.exit(1)

print('LedState Passed...')

#
#
#
#
#
#
#
#
#
#
#
#
#
#

print('Testing LedController...')
print('Warning: The led control server must be restarted before each test')
controller = LedController()

# get pre-initialized led
led = controller.get(26)
if led.r != 0 or led.g != 0 or led.b != 0 or led.a != .1:
    print('Pre-initialized failed, got led: {c}'.format(c=led.to_string()))
    sys.exit(1)


# create new led, update the set, then get the led back.
led = Led(26, 102, 0, 102, .3)
if not controller.set(led):
    print('Led update returned false')
    sys.exit(1)

led = controller.get(26)
if led.r != 102 or led.g != 0 or led.b != 102 or led.a != .3:
    print('Led update failed, got led: {c}'.format(c=led.to_string()))
    sys.exit(1)


# clear the colors and recheck
if not controller.clear():
    print('clear command returned false')

led = controller.get(26)
if led.r != 0 or led.g != 0 or led.b != 0 or led.a != .1:
    print('Failed to clear colors, got led: {c}'.format(c=led.to_string()))
    sys.exit(1)

print('LedController Passed...')



print('All tests passed')
