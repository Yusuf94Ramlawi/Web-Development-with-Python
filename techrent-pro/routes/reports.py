
import db
from flask import Blueprint, render_template
from collections import Counter

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
    # Revenue calculations
    total_revenue = sum(
        r["total_cost"] for r in db.rental_data.values()
        if r["status"] == "returned"
    )
    active_revenue = sum(
        r["total_cost"] for r in db.rental_data.values()
        if r["status"] == "active"
    )

    # Top 3 most-rented equipment (by number of rentals)
    equipment_rental_count = Counter()
    for rental in db.rental_data.values():
        equipment_rental_count[rental["equipment_id"]] += 1

    top_equipment = []
    for eq_id, count in equipment_rental_count.most_common(3):
        equipment = db.equipment_data.get(eq_id)
        if equipment:
            top_equipment.append({
                "name": equipment["name"],
                "category": equipment["category"],
                "rental_count": count,
            })

    # Top 3 customers by total spend
    customer_spending = {}
    for rental in db.rental_data.values():
        customer_id = rental["customer_id"]
        if customer_id not in customer_spending:
            customer_spending[customer_id] = 0
        customer_spending[customer_id] += rental["total_cost"]

    top_customers = []
    for customer_id, total in sorted(
        customer_spending.items(), key=lambda x: x[1], reverse=True
    )[:3]:
        customer = db.customer_data.get(customer_id)
        if customer:
            top_customers.append({
                "name": customer["name"],
                "email": customer["email"],
                "total_spent": total,
            })

    # Rentals by status
    status_counts = {"active": 0, "returned": 0, "overdue": 0}
    for rental in db.rental_data.values():
        status = rental.get("status", "active").lower()
        if status in status_counts:
            status_counts[status] += 1

    total_rentals = sum(status_counts.values())
    status_percentages = {}
    if total_rentals > 0:
        for status, count in status_counts.items():
            status_percentages[status] = round(
                (count / total_rentals) * 100, 1)
    else:
        status_percentages = {"active": 0, "returned": 0, "overdue": 0}

    return render_template(
        'reports/index.html',
        total_revenue=total_revenue,
        active_revenue=active_revenue,
        top_equipment=top_equipment,
        top_customers=top_customers,
        status_counts=status_counts,
        status_percentages=status_percentages,
        total_rentals=total_rentals,
    )
