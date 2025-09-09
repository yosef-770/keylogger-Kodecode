from flask import Blueprint, render_template, current_app, send_from_directory
import os

frontend_bp = Blueprint("frontend", __name__)

@frontend_bp.route("/")
def render_dashboard():
    return render_template("dashboard.html", base_url=current_app.config["BASE_URL"])

@frontend_bp.route("/favicon.ico")
def favicon():
    # Get the path to the static folder (one level up from backend/routes)
    static_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static')
    return send_from_directory(static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')
