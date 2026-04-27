from flask import Blueprint, render_template
from services import frontend_api_service

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")


@reports_bp.route('/')
def reports():
    """
    Render analytics and summary report metrics.

    Args:
        None

    Returns:
        Response: Rendered reports page.
    """
    status_code, payload = frontend_api_service.get('/api/reports/summary')

    if status_code != 200:
        payload = {
            "total_revenue": 0,
            "active_revenue": 0,
            "top_equipment": [],
            "top_customers": [],
            "status_counts": {"active": 0, "returned": 0, "overdue": 0},
            "status_percentages": {"active": 0, "returned": 0, "overdue": 0},
            "total_rentals": 0,
        }

    return render_template(
        'reports/index.html',
        total_revenue=payload.get('total_revenue', 0),
        active_revenue=payload.get('active_revenue', 0),
        top_equipment=payload.get('top_equipment', []),
        top_customers=payload.get('top_customers', []),
        status_counts=payload.get(
            'status_counts', {"active": 0, "returned": 0, "overdue": 0}),
        status_percentages=payload.get(
            'status_percentages', {"active": 0, "returned": 0, "overdue": 0}),
        total_rentals=payload.get('total_rentals', 0),
    )
