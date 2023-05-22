import fcntl
import os
import time
import json
from array import array
from led_color import Color

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    print("nope")
# end_try

class LedController:
    __filename = "/tmp/led-controller.state"

    def __init__(self):
        # create the file if it doesn't exist
        if not os.path.exists(self.__filename):
            os.mknod(self.__filename)
    # end_init

    def activate(self, index: int, color: Color):
        with open(self.__filename, 'r+') as handle:
            # Wait for lock
            fcntl.flock(handle, fcntl.LOCK_EX)

            # read file as json, modify json, truncate file, write file
            #contents = json.loads(handle.read())
            #handle.truncate()
            #handle.write("json")

            # release lock and close
            fcntl.flock(handle, fcntl.LOCK_UN)
            handle.close()
        # end_with
        # end_with
    # end_activate
# end_LedController



