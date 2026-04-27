"""Reports and analytics business logic."""
from collections import Counter
import db


def get_reports_summary():
    """
    Build reports and analytics data.

    Returns:
        dict: Report summary used by API and rendered pages.
    """
    total_revenue = sum(
        rental["total_cost"]
        for rental in db.rental_data.values()
        if rental["status"] == "returned"
    )
    active_revenue = sum(
        rental["total_cost"]
        for rental in db.rental_data.values()
        if rental["status"] == "active"
    )

    equipment_rental_count = Counter()
    for rental in db.rental_data.values():
        equipment_rental_count[rental["equipment_id"]] += 1

    top_equipment = []
    for equipment_id, count in equipment_rental_count.most_common(3):
        equipment = db.equipment_data.get(equipment_id)
        if equipment:
            top_equipment.append({
                "name": equipment["name"],
                "category": equipment["category"],
                "rental_count": count,
            })

    customer_spending = {}
    for rental in db.rental_data.values():
        customer_id = rental["customer_id"]
        customer_spending[customer_id] = (
            customer_spending.get(customer_id, 0) + rental["total_cost"]
        )

    top_customers = []
    for customer_id, total in sorted(
        customer_spending.items(),
        key=lambda item: item[1],
        reverse=True,
    )[:3]:
        customer = db.customer_data.get(customer_id)
        if customer:
            top_customers.append({
                "name": customer["name"],
                "email": customer["email"],
                "total_spent": total,
            })

    status_counts = {"active": 0, "returned": 0, "overdue": 0}
    for rental in db.rental_data.values():
        status = rental.get("status", "active").lower()
        if status in status_counts:
            status_counts[status] += 1

    total_rentals = sum(status_counts.values())
    if total_rentals > 0:
        status_percentages = {
            status: round((count / total_rentals) * 100, 1)
            for status, count in status_counts.items()
        }
    else:
        status_percentages = {"active": 0, "returned": 0, "overdue": 0}

    return {
        "total_revenue": total_revenue,
        "active_revenue": active_revenue,
        "top_equipment": top_equipment,
        "top_customers": top_customers,
        "status_counts": status_counts,
        "status_percentages": status_percentages,
        "total_rentals": total_rentals,
    }
