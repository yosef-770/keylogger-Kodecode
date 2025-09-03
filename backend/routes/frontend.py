from flask import Blueprint, render_template, current_app

frontend_bp = Blueprint("frontend", __name__)

@frontend_bp.route("/")
def render_dashboard():
    return render_template("dashboard.html", base_url=current_app.config["BASE_URL"])
