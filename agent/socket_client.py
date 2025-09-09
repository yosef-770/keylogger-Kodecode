import os

import socketio
from dotenv import load_dotenv

from agent.client_details import get_client_details, get_display_username

load_dotenv()


def init_socket(debug=False):
    base_url = os.getenv("BASE_URL") if debug else 'https://project.kodcode.co.il'
    sio = socketio.Client()
    client_details = get_client_details()
    username = get_display_username()
    sio.connect(
        base_url,
        headers=client_details,
        transports=['websocket'],
        namespaces=['/'],
        auth=username,
        retry=True
    )
    print(f'''\033[32m ◎ ◉ Connected to \033[31m{"development" if debug else "production"}\033[32m server: [{base_url}/] ◎ ◉ \033[0m''')
    return sio

def reconnect(debug=False):
    sio = None
    while sio is None or not sio.connected:
        print("Reconnecting...")
        sio = init_socket(debug)
    return sio