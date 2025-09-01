from datetime import datetime

from flask import Flask, request, jsonify

from db import DB

app = Flask(__name__)
db = DB()

# get
@app.route("/logs")
def logs():
    offset = request.args.get('offset', default=0, type=int)
    limit = request.args.get('limit', type=int)
    all_logs = db.fetch_logs(offset=offset, limit=limit)
    return jsonify(logs=all_logs)

@app.route("/logs/user")
def get_all_usernames():
    offset = request.args.get('offset', default=0, type=int)
    limit = request.args.get('limit', type=int)
    usernames = db.get_all_usernames(offset=offset, limit=limit)
    return jsonify(usernames=usernames)

@app.route("/logs/user/<string:username>")
def get_logs_by_username(username):
    offset = request.args.get('offset', default=0, type=int)
    limit = request.args.get('limit', type=int)
    user_logs = db.get_by_username(username, offset=offset, limit=limit)
    return jsonify(logs=user_logs)

@app.route("/logs/machine")
def get_all_machines():
    offset = request.args.get('offset', default=0, type=int)
    limit = request.args.get('limit', type=int)
    machines = db.get_all_machines(offset=offset, limit=limit)
    return jsonify(machines=machines)

@app.route("/logs/machine/<string:machine>")
def get_logs_by_machine(machine):
    offset = request.args.get('offset', default=0, type=int)
    limit = request.args.get('limit', type=int)
    machine_logs = db.get_by_machine(machine, offset=offset, limit=limit)
    return jsonify(logs=machine_logs)

@app.route("/logs/date")
def get_logs_by_date_range():
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    offset = request.args.get('offset', default=0, type=int)
    limit = request.args.get('limit', type=int)
    if not start_date or not end_date:
        return jsonify({"error": "Please provide both start and end date in YYYY-MM-DD format"}), 400

    date_logs = db.get_by_date_range(start_date, end_date, offset=offset, limit=limit)
    return jsonify(logs=date_logs)

@app.route("/search")
def search_text():
    query = request.args.get('q', '')
    offset = request.args.get('offset', default=0, type=int)
    limit = request.args.get('limit', type=int)
    if not query:
        return jsonify({"error": "Please provide a search query parameter 'q'"}), 400

    search_results = db.search_text(query, offset=offset, limit=limit)
    return jsonify(logs=search_results)

# post
@app.route("/logs", methods=['POST'])
def add_log():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    print(data)

    timestamp = data.get("time", str(datetime.now()))
    events = data.get("events", [])
    username = data.get("username", "unknown")
    machine = data.get("machine")
    if timestamp and events:
        db.insert_log(timestamp, events if type(events) == str else "".join(events), username, machine)

    return jsonify({"message": "Logs added successfully"}), 201


# delete
@app.route("/logs/<int:log_id>", methods=['DELETE'])
def delete_log(log_id):
    db.delete_log(log_id)
    return jsonify({"message": f"Log {log_id} deleted successfully"}), 200

@app.route("/")
def hello_world():
    return jsonify({
        "message": "Welcome to Keyboard Tracking API",
        "endpoints": {
            "GET /logs": "Fetch all logs",
            "POST /logs": "Add new logs"
        }
    })


if __name__ == "__main__":
    app.run()