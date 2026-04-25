import db
from flask import Blueprint, render_template

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/")
def index():
    customers = db.customer_data
    equipments = db.equipment_data
    rentals = db.rental_data
    
    total_equipment = len(equipments)
    total_customers = len(customers)
    total_active_rentals = len([rental for rental in rentals.values() if rental["status"] == "active"])
    available_equipment = len([equipment for equipment in equipments.values() if equipment["available"] == True])


    recent_rentals = sorted(rentals.values(), key=lambda x: x["id"], reverse=True)[:5]
    
    recent_rentals_detailed = []
    for rental in recent_rentals:
        customer = customers.get(rental["customer_id"], {})
        equipment = equipments.get(rental["equipment_id"], {})
        recent_rentals_detailed.append({
            "id": rental["id"],
            "customer_name": customer.get("name", "Unknown"),
            "equipment_name": equipment.get("name", "Unknown"),
            "start_date": rental["start_date"],
            "end_date": rental["end_date"],
            "status": rental["status"].lower(),
            "total_cost": rental["total_cost"]
        })
    

    return render_template(
        "index.html",
        total_equipment=total_equipment,
        total_customers=total_customers,
        total_active_rentals=total_active_rentals,
        available_equipment=available_equipment,
        recent_rentals=recent_rentals_detailed
    )