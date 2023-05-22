import asyncio
import signal
import sys
import led_sockets
from led_state import LedState
from led import Led

# This server is intended to run on startup and never stop
# It listens for requests to get or set the state of the LEDs.


led_state = None
write_server = None
read_server = None


def handle_signal(sig, frame):
    try:
        write_server.close()
    finally:
        pass
    # end_try

    try:
        read_server.close()
    finally:
        sys.exit(0)
    # end_try
# handle_signal


signal.signal(signal.SIGINT, handle_signal)


async def handle_write(reader, writer):
    message = ''
    while True:
        data = await reader.read(led_sockets.chunk_size)
        if data:
            message += data.decode('ascii')
        else:
            writer.close()
            await writer.wait_closed()
            break
        # end_if
    # end_while

    if message == 'clear':
        led_state.clear()
    elif len(message) > 0:
        parts = message.split('|')
        for part in parts:
            led = Led.deserialize(part)
            led_state.set(led)
        # end_for
    # end_if
# handle_write


async def handle_read(reader, writer):
    try:
        message = ''
        while True:
            data = await reader.read(led_sockets.chunk_size)
            if data:
                message += data.decode('ascii')
            else:
                break
            # end_if
        # end_while

        if len(message) > 0:
            results = ''
            parts = message.split('|')
            for part in parts:
                id = int(part)
                led = led_state.get_by_id(id)
                if len(results) > 0:
                    results += '|'
                results += led.serialize()
            # end_for

            writer.write(bytes(results, 'ascii'))
        # end_if

        await writer.drain()
    except any:
        pass
    finally:
        writer.close()
        await writer.wait_closed()
    # end_try
# handle_read


async def main():
    global led_state
    global write_server
    global read_server

    led_state = LedState()
    write_server = await asyncio.start_unix_server(handle_write, led_sockets.write_address)
    read_server = await asyncio.start_unix_server(handle_read, led_sockets.read_address)

    async with write_server:
        await write_server.serve_forever()
    # end_with

    async with read_server:
        await read_server.serve_forever()
    # end_with
# main

asyncio.run(main())
