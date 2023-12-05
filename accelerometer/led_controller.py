import board
import neopixel


class LedController:
    _pixel_pin = board.D18
    _num_pixels = 50
    _pixels = None
    _off = (0, 0, 0)

    def __init__(self):
        PIXEL_PIN = self._pixel_pin
        NUM_PIXELS = self._num_pixels
        ORDER = neopixel.RGB

        self._pixels = neopixel.NeoPixel(
            PIXEL_PIN, NUM_PIXELS, brightness=1, auto_write=True, pixel_order=ORDER
        )
    # __init__

    def clear(self) -> bool:
        return self._pixels.fill(self._off)
    # clear

    def set(self, led_id: int, r: int = 0, g: int = 0, b: int = 0, a: float = .1) -> bool:
        if 0 <= led_id < self._num_pixels and 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255 and 0 <= a <= 1:
            self._pixels[led_id] = (r * a, g * a, b * a)
            return True
        else:
            return False
        # end_if
    # set

    def set_all(self, r: int = 0, g: int = 0, b: int = 0, a: float = .1) -> bool:
        if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255 and 0 <= a <= 1:
            self._pixels.fill((r * a, g * a, b * a))
            return True
        else:
            return False
        # end_if
    # set_all
# LedController
