"""Dashboard analytics business logic."""
import db


def get_dashboard_summary():
    """
    Build dashboard aggregates and recent rentals.

    Returns:
        dict: Dashboard summary data used by API and rendered pages.
    """
    customers = db.customer_data
    equipment = db.equipment_data
    rentals = db.rental_data

    total_equipment = len(equipment)
    total_customers = len(customers)
    total_active_rentals = len(
        [rental for rental in rentals.values() if rental["status"] == "active"]
    )
    available_equipment = len(
        [item for item in equipment.values() if item["available"]]
    )

    recent_rentals = sorted(
        rentals.values(),
        key=lambda item: item["id"],
        reverse=True,
    )[:5]

    recent_rentals_detailed = []
    for rental in recent_rentals:
        customer = customers.get(rental["customer_id"], {})
        item = equipment.get(rental["equipment_id"], {})
        recent_rentals_detailed.append({
            "id": rental["id"],
            "customer_name": customer.get("name", "Unknown"),
            "equipment_name": item.get("name", "Unknown"),
            "start_date": rental["start_date"],
            "end_date": rental["end_date"],
            "status": rental["status"].lower(),
            "total_cost": rental["total_cost"],
        })

    return {
        "total_equipment": total_equipment,
        "total_customers": total_customers,
        "total_active_rentals": total_active_rentals,
        "available_equipment": available_equipment,
        "recent_rentals": recent_rentals_detailed,
    }
