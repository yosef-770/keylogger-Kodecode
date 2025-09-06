from flask import Blueprint, request, jsonify

from backend.data.repository import db_manager

api_bp = Blueprint("api", __name__)

@api_bp.route("/connections")
def get_connections():
    offset = request.args.get('offset', default=0, type=int)
    limit = request.args.get('limit', type=int)

    username = request.args.get('username')
    machine = request.args.get('machine')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    search_query = request.args.get('q')
    status = request.args.get('status')
    status = status if status in ['open', 'closed'] else None

    if any([username, machine, start_date, end_date, status]):
        all_logs = db_manager.get_connections(
            username=username,
            machine=machine,
            start_date=start_date,
            end_date=end_date,
            offset=offset,
            limit=limit,
            status=status
        )
    else:
        all_logs = db_manager.get_connections(offset=offset, limit=limit)

    return jsonify(logs=all_logs)

@api_bp.route("/logs/<int:log_id>", methods=['DELETE'])
def delete_log(log_id):
    db_manager.delete_log(log_id)
    return jsonify({"message": f"Log {log_id} deleted successfully"}), 200

@api_bp.route("/connections/<int:connection_id>", methods=['DELETE'])
def delete_connection(connection_id):
    db_manager.delete_connection(connection_id)
    return jsonify({"message": f"Connection {connection_id} deleted successfully"}), 200




# TODO add support to get list of users and machines
# TODO add search

