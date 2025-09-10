from curses.ascii import isdigit

from flask import Blueprint, request, jsonify, abort

from backend.data.database_manager import database_manager

machines_bp = Blueprint("machines", __name__)

@machines_bp.route("/")
def get_machines():
    offset = request.args.get('offset', default=0, type=int)
    limit = request.args.get('limit', type=int)

    username = request.args.get('username')
    title = request.args.get('title')

    status = request.args.get('status')
    status = int(status) if status and isdigit(status) else None

    if any([username, title, status]):
        machines = database_manager.machine_repo.get_machines(
            username=username,
            title=title,
            offset=offset,
            limit=limit,
            status=status
        )
    else:
        machines = database_manager.machine_repo.get_machines(offset=offset, limit=limit)

    return jsonify(machines)

@machines_bp.route("/<int:machine_id>")
def get_machine_by_id(machine_id):
    machine = database_manager.machine_repo.get_machine_by_id(machine_id)
    if machine:
        return jsonify(machine), 200
    abort(404)


@machines_bp.route("/<string:username>")
def get_machine_by_username(username):
    machine = database_manager.machine_repo.get_machine_by_username(username)
    if machine:
        return jsonify(machine), 200
    abort(404)


@machines_bp.route("/<string:username>/title", methods=["POST"])
def set_machine_title(username):
    title = request.get_json().get("title")
    database_manager.machine_repo.set_title(username, title)
    return jsonify({}), 200


