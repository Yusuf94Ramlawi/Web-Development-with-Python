from flask import Blueprint, render_template
from services import frontend_api_service

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/")
def index():
    """
    Render dashboard metrics and recent rentals.

    Args:
        None

    Returns:
        Response: Rendered dashboard page.
    """
    status_code, payload = frontend_api_service.get('/api/dashboard/summary')

    if status_code != 200:
        payload = {
            "total_equipment": 0,
            "total_customers": 0,
            "total_active_rentals": 0,
            "available_equipment": 0,
            "recent_rentals": [],
        }

    return render_template(
        "index.html",
        total_equipment=payload.get("total_equipment", 0),
        total_customers=payload.get("total_customers", 0),
        total_active_rentals=payload.get("total_active_rentals", 0),
        available_equipment=payload.get("available_equipment", 0),
        recent_rentals=payload.get("recent_rentals", []),
    )
