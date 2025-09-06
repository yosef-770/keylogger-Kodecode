import sys

from pynput import keyboard

from agent import key_handler
from agent.print_credit import print_welcome
from agent.socket_client import init_socket, disconnect_handler

debug = 'debug' in sys.argv # run with "python app.py debug" for local testing
sio = init_socket(debug)


def launch():
    print_welcome()

    sio.on('connect', lambda: print('Connected to server'))
    sio.on('disconnect', lambda: disconnect_handler())
    sio.on('res', lambda data: print('Message from server:', data))
    listener = keyboard.Listener(on_press=lambda key: key_handler.on_key(key, sio))
    listener.start()

    sio.wait()

def main():
    try:
        launch()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        sio.disconnect()
