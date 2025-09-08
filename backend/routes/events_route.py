from itertools import count

from flask import Blueprint, request, jsonify

from backend.data.database_manager import database_manager

events_bp = Blueprint("events", __name__)

@events_bp.route("/<int:machine_id>")
def get_events_by_machine_id(machine_id):
    offset = request.args.get('offset', default=0, type=int)
    limit = request.args.get('limit', type=int)

    events = database_manager.event_repo.get_events_by_machine_id(machine_id, offset, limit)

    return jsonify(events), 200

@events_bp.route("/<int:machine_id>/count")
def get_count_by_machine_id(machine_id):
    count = database_manager.event_repo.get_count_by_machine_id(machine_id)
    print(count)
    return jsonify(count= count), 200