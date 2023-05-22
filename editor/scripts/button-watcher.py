import time
import board
import RPi.GPIO as GPIO
import subprocess
import psutil

launcher_pin = 23
launcher_pin_state = 0

accel_left_btn_pin = 17
accel_left_btn_pin_state = 0

while True:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # Use physical pin numbering
    GPIO.setup(launcher_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(accel_left_btn_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # if the button is not pressed
    if GPIO.input(launcher_pin):
        launcher_pin_state = 0
    else:
        if launcher_pin_state is 0:
            launcher_pin_state = 1
            exec(open("/home/pi/launcher_btn_press.py").read())
        # end_if
    # end_ if


    # if the button is not pressed
    if GPIO.input(accel_left_btn_pin):
        accel_left_btn_pin_state = 0
    else:
        if accel_left_btn_pin_state is 0:
            accel_left_btn_pin_state = 1
            exec(open("/home/pi/accel_left_btn_press.py").read())
        # end_if
    # end_ if

    time.sleep(.1)
# end_if
