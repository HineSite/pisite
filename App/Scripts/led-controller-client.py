# https://pymotw.com/2/socket/uds.html

import socket
import sys
import time

# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_write_address = '/tmp/led-controller-write'
server_read_address = '/tmp/led-controller-read'

def write():
    try:
        sock.connect(server_write_address)
    except socket.error as msg:
        print('connection error %s', msg)
        sys.exit(1)

    try:
        time.sleep(20)
        # Send data
        message = 'This is the message1'
        print('sending "{s}"'.format(s=message))
        sock.sendall(bytes(message, 'ascii'))

    finally:
        print('closing socket')
        sock.close()


def read():
    try:
        sock.connect(server_read_address)
    except socket.error as msg:
        print('connection error %s', msg)
        sys.exit(1)

    try:
        message = '16'
        print('sending "{s}"'.format(s=message))
        sock.sendall(bytes(message, 'ascii'))

        response = ''
        while True:
            data = sock.recv(16)
            if data:
                response += data.decode('ascii')
            else:
                print('response: {s}'.format(s=response))
                break
            # end_if
        # end_while

    finally:
        print('closing socket')
        sock.close()


if sys.argv[1] == "write":
    write()

if sys.argv[1] == "read":
    read()
