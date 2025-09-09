import logging
import multiprocessing
import threading
from multiprocessing import Queue

from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

from backend.routes.events_route import events_bp
from backend.routes.machines_route import machines_bp
from backend.routes.frontend import frontend_bp
from backend.data.queue_manager import db_worker
from backend.socket_handlers import register_socket_handlers
from backend.config import Config

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':

    # DB worker thread
    event_queue = Queue()
    worker_process = multiprocessing.Process(target=db_worker, args=(event_queue,))
    worker_process.daemon = True
    worker_process.start()
    print("DB Worker thread started")

    # Flask
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS for all routes
    CORS(app)

    app.jinja_env.variable_start_string = '[['
    app.jinja_env.variable_end_string = ']]'

    app.register_blueprint(machines_bp, url_prefix="/api/machines")
    app.register_blueprint(events_bp, url_prefix="/api/events")
    app.register_blueprint(frontend_bp)

    socketio = SocketIO(app, cors_allowed_origins="*")
    register_socket_handlers(socketio, event_queue)

    socketio.run(app, allow_unsafe_werkzeug=True, debug=False)
