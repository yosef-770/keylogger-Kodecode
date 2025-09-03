import os
import sys

import socketio
from dotenv import load_dotenv

from client_details import get_client_details

load_dotenv()


def init_socket(debug=False):
    url = os.getenv("BASE_URL") if debug else 'https://project.kodcode.co.il'
    sio = socketio.Client()
    client_details = get_client_details()
    sio.connect(url, headers=client_details)
    return sio



def disconnect_handler():
    """ Handle disconnection from server, exit program.
    """
    print('Disconnected from server, shut down.')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)