# https://pymotw.com/2/socket/uds.html

import socket
import sys
import os
import signal
import time

write_address = '/tmp/led-controller-write'  # socket used to listen for write requests
read_address = '/tmp/led-controller-read'  # socket used to listed for read requests
write_connection = None
read_connection = None
chunk_size = 16
results = ''
running = True


def handle_signal(sig, frame):
    global running
    try:
        running = False
    finally:
        sys.exit(0)
    # end_try
# handle_signal


signal.signal(signal.SIGINT, handle_signal)


try:
    os.unlink(write_address)
except OSError:
    if os.path.exists(write_address):
        raise
    # end_if
# end_try

try:
    os.unlink(read_address)
except OSError:
    if os.path.exists(read_address):
        raise
    # end_if
# end_try





import selectors

def handle_write(sock, mask):
    global results
    print('waiting to accept')
    with sock.accept()[0] as client:
        print('accepted connection')
        message = ''
        while True:
            data = client.recv(chunk_size)
            time.sleep(.2)
            if data:
                message += data.decode('ascii')
            else:
                results = message
                print('message received: {s}'.format(s=message))
                break
            # end_if
        # end_while
    # end_with
# handle_write


def handle_read(sock, mask):
    global results
    print('waiting to read')
    with sock.accept()[0] as client:
        print('reading to connected')
        led_id = -1
        data = client.recv(4)
        if not data:
            client.sendall('invalid message. You must only send a single led id')
        else:
            led_id = data.decode('ascii')
            print('led id: {s}'.format(s=led_id))
            client.sendall(bytes(results, 'ascii'))
        # end_if
    # end_with
# handle_read



sel = selectors.DefaultSelector()
def add_write():
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(write_address)
    sock.listen(10)
    sock.setblocking(False)
    sel.register(sock, selectors.EVENT_READ, handle_write)

def add_read():
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(read_address)
    sock.listen(10)
    sock.setblocking(False)
    sel.register(sock, selectors.EVENT_READ, handle_read)


add_write()
add_read()


while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)





















from threading import Thread
# def main():
#     print("start me")
#
#     write_thread = Thread(name='led_controller_write_listener', target=write)
#     write_thread.run()
#
#     print("no wait")
#
#     read_thread = Thread(name='led_controller_read_listener', target=read)
#     read_thread.run()
#
#     print("end me")
#     signal.pause()
#
# def write():
#     global results
#
#     with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
#         sock.bind(write_address)
#         sock.listen(10)
#         #sock.setblocking(False)
#         while running:
#             print('waiting')
#             with sock.accept()[0] as client:
#                 print('connected w')
#                 message = ''
#                 while True:
#                     data = client.recv(chunk_size)
#                     if data:
#                         message += data.decode('ascii')
#                     else:
#                         results = message
#                         print('message received: {s}'.format(s=message))
#                         break
#                     # end_if
#                 # end_while
#
#
# def read():
#     global results
#
#     print('rainbows')
#     with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
#         sock.bind(read_address)
#         sock.listen(10)
#         #sock.setblocking(False)
#         while running:
#             print('reading')
#             with sock.accept()[0] as client:
#                 print('connected r')
#                 led_id = -1
#                 data = client.recv(chunk_size)
#                 if not data:
#                     client.sendall('invalid message. You must only send a single led id')
#                 else:
#                     led_id = data.decode('ascii')
#                     print('led id: {s}'.format(s=led_id))
#                     client.sendall(results)
#                     break
#                 # end_if
#
# main()























# # Make sure the socket does not already exist
# try:
#     os.unlink(write_address)
#     os.unlink(read_address)
# except OSError:
#     if os.path.exists(write_address) or os.path.exists(read_address):
#         raise
#     # end_if
# # end_try
#
#
# # Create a UDS socket
# write_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
# read_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#
# write_socket.bind(write_address)
# read_socket.bind(read_address)
#
# # Listen for incoming connections
# write_socket.listen(10)
# read_socket.listen(10)
#
#
# def main():
#     print("it begins")
#     try:
#         asyncio.ensure_future(listen_for_writer())
#         asyncio.ensure_future(listen_for_reader())
#         loop.run_forever()
#     except KeyboardInterrupt:
#         pass
#     finally:
#         print("Closing Loop")
#         loop.close()
#     print("it ends")
#
#
# async def async_main():
#     print("in async_main")
#     await asyncio.gather(listen_for_writer(), listen_for_reader())
#     print("outing async_main")
#
#
#
# async def listen_for_writer():
#     global write_connection
#
#     while True:
#         try:
#             print('waiting for writer')
#             write_connection = write_socket.accept()[0]
#
#             message = ''
#             while True:
#                 data = write_connection.recv(chunk_size)
#                 if data:
#                     message += data.decode('ascii')
#                 else:
#                     print('message received: {s}'.format(s=message))
#                     break
#                 # end_if
#             # end_while
#         finally:
#             # Clean up the connection
#             write_connection.close()
#         # end_finally
#     # end_while
# # listen_for_writer
#
#
# async def listen_for_reader():
#     global read_connection
#
#     while True:
#         try:
#             print('waiting for reader')
#             read_connection = read_socket.accept()[0]
#
#             message = ''
#             while True:
#                 data = read_connection.recv(chunk_size)
#                 if data:
#                     message += data.decode('ascii')
#                 else:
#                     print('request received: {s}'.format(s=message))
#                     read_connection.sendall(bytes(results, 'ascii'))
#                     break
#                 # end_if
#             # end_while
#         finally:
#             # Clean up the connection
#             read_connection.close()
#         # end_finally
#     # end_while
# # listen_for_writer
#
#
# main()
