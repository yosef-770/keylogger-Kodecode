from os import getenv
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, session
from flask_socketio import SocketIO, emit

from db import DB

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.jinja_env.variable_start_string = '[['
app.jinja_env.variable_end_string = ']]'
socketio = SocketIO(app)

db = DB(db_name=getenv("DQLITE_PATH"))

# get
@app.route("/connections")
def logs():
    offset = request.args.get('offset', default=0, type=int)
    limit = request.args.get('limit', type=int)
    
    username = request.args.get('username')
    machine = request.args.get('machine')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    search_query = request.args.get('q')
    status = request.args.get('status')
    status = status if  status in ['open', 'closed'] else None
    
    if any([username, machine, start_date, end_date, status]):
        all_logs = db.get_connections(
            username=username,
            machine=machine,
            start_date=start_date,
            end_date=end_date,
            offset=offset,
            limit=limit,
            status=status
        )
    else:
        all_logs = db.get_connections(offset=offset, limit=limit)
    
    return jsonify(logs=all_logs)

# TODO add support to get list of users and machines
# TODO add search


# delete
@app.route("/logs/<int:log_id>", methods=['DELETE'])
def delete_log(log_id):
    db.delete_log(log_id)
    return jsonify({"message": f"Log {log_id} deleted successfully"}), 200

@app.route("/connections/<int:connection_id>", methods=['DELETE'])
def delete_connection(connection_id):
    db.delete_connection(connection_id)
    return jsonify({"message": f"Connection {connection_id} deleted successfully"}), 200



@app.route("/")
def render_dashboard():
    return render_template("dashboard.html", base_url = getenv("BASE_URL"))



# --------- WS ------------

# ws hand-shake
@socketio.on('connect')
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
    connection_id = db.init_connection(timestamp, username, processor, system, node, release, version, machine, ip_address)

    session['connection_id'] = connection_id
    print("New connection:", connection_id, username, ip_address)

@socketio.on('disconnect')
def handle_disconnect():
    connection_id = session.get('connection_id')
    print("Client disconnected:", connection_id)
    if connection_id:
        db.close_connection(connection_id)
        print("Connection closed:", connection_id)

# ws event
@socketio.on('ev')
def handle_event(message):
    print(f'Received event from {session.get("connection_id")}: {message}')
    connection_id = int(session.get('connection_id'))
    timestamp = int(datetime.now().timestamp())
    if connection_id:
        db.insert_log(connection_id, timestamp, message['ev'])
        emit('ack', {'status': 'received'})

if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True, debug=False)