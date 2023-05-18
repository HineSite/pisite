import fcntl
import os
import time
import json
from array import array

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    print("nope")
# end_try


class Color:
    R: int = 0
    G: int = 0
    B: int = 0
    A: int = 25

    def __init__(self, r: int, g: int, b: int, a: int = 25):
        self.R = r
        self.G = g
        self.B = b
        self.A = a
    # end_init

    def array(self) -> array[int]:
        return self.R, self.G, self.B, self.A
    # end_init
# end_color


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



