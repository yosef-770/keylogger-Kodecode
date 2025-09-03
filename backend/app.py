import queue
import threading

from flask import Flask
from flask_socketio import SocketIO

from backend.routes.api import api_bp
from backend.routes.frontend import frontend_bp
from db.event_queue import db_worker
from db.db import DB
from socket_handlers import register_socket_handlers
from config import Config

# db setup
db = DB(Config.DQLITE_PATH)

# Event queue setup
event_queue = queue.Queue()

# Flask config
app = Flask(__name__)
app.config.from_object(Config)

app.jinja_env.variable_start_string = '[['
app.jinja_env.variable_end_string = ']]'

app.register_blueprint(api_bp, url_prefix="/api")
app.register_blueprint(frontend_bp)

# SocketIO setup
socketio = SocketIO(app, cors_allowed_origins="*")
register_socket_handlers(socketio, db=db, event_queue=event_queue)


if __name__ == '__main__':
    # Start the DB worker thread
    threading.Thread(target=db_worker, daemon=True).start()

    # Run the Flask app with SocketIO
    socketio.run(app, allow_unsafe_werkzeug=True, debug=False)