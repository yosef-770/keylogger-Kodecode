import sys
import keyboard

import get_key
from print_credit import print_welcome
from socket_client import init_socket, disconnect_handler

debug = 'debug' in sys.argv # run with "python main.py debug" for local testing
sio = init_socket(debug)


def main():
    print_welcome()

    sio.on('connect', lambda: print('Connected to server'))
    sio.on('disconnect', lambda: disconnect_handler())
    sio.on('res', lambda data: print('Message from server:', data))
    keyboard.on_press(lambda e: get_key.on_key(e, sio))

    sio.wait()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        sio.disconnect()
