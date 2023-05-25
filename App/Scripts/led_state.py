from led import Led

_has_pixels = True

try:
    import board
    import neopixel
except ImportError:
    _has_pixels = False
# end_try


class LedState:
    led_state = None
    pixels = None

    def __init__(self):
        self.led_state = [Led()] * 50

        if _has_pixels:
            self.pixels = neopixel.NeoPixel(board.D18, 50, brightness=1, auto_write=True, pixel_order=neopixel.RGB)
            self.pixels.fill((0, 0, 0))
        # end_if
    # __init__

    def get_by_id(self, id: int) -> Led:
        return self.led_state[id]
    # get_by_id

    def clear(self) -> None:
        self.led_state = [Led()] * 50

        if _has_pixels:
            self.pixels.fill((0, 0, 0))
        # end_if
    # clear

    def set(self, led: Led) -> None:
        self.led_state[led.id] = led

        if _has_pixels:
            r = round(led.r * led.a)
            g = round(led.g * led.a)
            b = round(led.b * led.a)

            self.pixels[led.id] = (r, g, b)
        # end_if
    # set_by_id
# LedState
