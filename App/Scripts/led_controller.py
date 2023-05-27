import socket
import led_sockets
from array import array
from led import Led


class LedController:
    _eol = '\n'  # just don't run it on windows...

    def __init__(self):
        pass
    # __init__

    def _connect(self, address: str, message: str) -> str | None:
        sock = None

        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(address)
            sock.sendall(bytes(message + self._eol, 'ascii'))
            sock.shutdown(socket.SHUT_WR)

            response = ''
            while True:
                data = sock.recv(led_sockets.chunk_size)
                if data:
                    response += data.decode('ascii')
                else:
                    sock.shutdown(socket.SHUT_RDWR)
                    break
                # end_if
            # end_while

            return response
        except socket.error as msg:
            print('socket connection error error on {add}. Error: {err}'.format(add=address, err=msg))
            return None
        finally:
            if sock:
                sock.close()
        # end_try
    # _connect

    def _write(self, message) -> bool:
        response = self._connect(led_sockets.write_address, message)
        return response == ''
    # write

    def _read(self, message) -> [Led()]:
        response = self._connect(led_sockets.read_address, message)
        if not response or len(response) == 0:
            return None

        leds = []
        parts = response.split('|')
        for part in parts:
            led = Led.deserialize(part)
            leds.append(led)
        # end_for

        return leds
    # read

    def set(self, led: Led) -> bool:
        return self._write(led.serialize())
    # write

    def clear(self) -> bool:
        return self._write('clear')
    # write

    def get(self, id: int) -> Led:
        message = '{id}'.format(id=id)
        leds = self._read(message)
        return leds[0]
    # write

    def get_all(self) -> array:
        leds = self._read('')
        return leds
    # write
# LedController
