from itertools import count

from flask import Blueprint, request, jsonify

from backend.data.database_manager import database_manager

events_bp = Blueprint("events", __name__)

@events_bp.route("/<int:machine_id>")
def get_events_by_machine_id(machine_id):
    offset = request.args.get('offset', default=0, type=int)
    limit = request.args.get('limit', type=int)
    
    print(f"Getting events for machine {machine_id}, offset={offset}, limit={limit}")
    try:
        events = database_manager.event_repo.get_events_by_machine_id(machine_id, offset, limit)
        print(f"Found {len(events)} events for machine {machine_id}")
        return jsonify(events), 200
    except Exception as e:
        print(f"Error getting events for machine {machine_id}: {str(e)}")
        return jsonify(error=f"Error getting events: {str(e)}"), 500

@events_bp.route("/<int:machine_id>/count")
def get_count_by_machine_id(machine_id):
    try:
        count = database_manager.event_repo.get_count_by_machine_id(machine_id)
        print(f"Count for machine {machine_id}: {count}")
        return jsonify(count=count), 200
    except Exception as e:
        print(f"Error getting count for machine {machine_id}: {str(e)}")
        return jsonify(error=f"Error getting count: {str(e)}"), 500