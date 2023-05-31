import asyncio
import os
import signal
import sys
import led_sockets
from led_state import LedState
from led import Led

# This server is intended to run on startup and never stop
# It listens for requests to get or set the state of the LEDs.

debug = True if len(sys.argv) > 1 and sys.argv[1] == 'debug' else False

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


def debug(message):
    if debug:
        print(message)
    # end_if
# debug


async def handle_write(reader, writer):
    debug('Write request received')

    message = ''
    data = await reader.readline()
    if data and len(data) > 1:
        message += data[:-1].decode('ascii')
        debug('Write request: {m}'.format(m=message))
    else:
        debug('Write request failed (no data): {d}'.format(d=data))
    # end_if

    writer.close()
    await writer.wait_closed()

    if message == 'clear':
        debug('Clearing leds')
        led_state.clear()
    elif len(message) > 0:
        debug('Parsing parts to write led state')
        parts = message.split('|')
        for part in parts:
            led = Led.deserialize(part)
            led_state.set(led)
        # end_for
    # end_if

    debug('Write request complete')
# handle_write


async def handle_read(reader, writer):
    debug('Read request received')
    try:
        message = ''
        data = await reader.readline()
        if data and len(data) > 1:
            message += data[:-1].decode('ascii')
            debug('Read request: {m}'.format(m=message))
        else:
            debug('Read request failed (no data): {d}'.format(d=data))
        # end_if

        if len(message) > 0:
            results = ''
            if message == 'all':
                debug('Serializing all LEDs')
                results = led_state.serialize_all()
            else:
                debug('Parsing parts to read led state')
                parts = message.split('|')
                for part in parts:
                    id = int(part)
                    led = led_state.get_by_id(id)
                    if len(results) > 0:
                        results += '|'
                    results += led.serialize()
                # end_for
            # end_if

            debug('Sending led states to client: {r}'.format(r=results))
            writer.write(bytes(results, 'ascii'))
        # end_if

        await writer.drain()
    except Exception as e:
        debug('Unhandled exception: {m}'.format(m=str(e)))
    finally:
        writer.close()
        await writer.wait_closed()
    # end_try

    debug('Read request complete')
# handle_read


async def main():
    global led_state
    global write_server
    global read_server

    debug('Server Started')

    led_state = LedState()
    write_server = await asyncio.start_unix_server(handle_write, led_sockets.write_address)
    read_server = await asyncio.start_unix_server(handle_read, led_sockets.read_address)

    os.chmod(led_sockets.write_address, 0o666)
    os.chmod(led_sockets.read_address, 0o666)

    async with write_server:
        await write_server.serve_forever()
    # end_with

    async with read_server:
        await read_server.serve_forever()
    # end_with
# main

asyncio.run(main())
