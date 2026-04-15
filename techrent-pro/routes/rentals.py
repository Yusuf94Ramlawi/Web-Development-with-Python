import datetime
import db
from flask import Blueprint, jsonify, render_template, request

rentals_bp = Blueprint("rentals", __name__)


def calculate_total_cost(equipment_id, start_date, end_date):
    equipment = db.equipment_data.get(int(equipment_id))
    if not equipment:
        return 0.0

    daily_rate = equipment.get("daily_rate", 0.0)
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    days = (end - start).days + 1
    return round(daily_rate * days, 2)

def check_overlap_booking(equipment_id, start_date, end_date):
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    for rental in db.rental_data.values():
        if rental["equipment_id"] == int(equipment_id) and rental["status"] == "active":
            existing_start = datetime.datetime.strptime(rental["start_date"], "%Y-%m-%d")
            existing_end = datetime.datetime.strptime(rental["end_date"], "%Y-%m-%d")

            if (start <= existing_end and end >= existing_start):
                return True

    return False

def validate_rental_payload(payload, partial=False):
    required_fields = [
        "equipment_id",
        "customer_id",
        "start_date",
        "end_date",
        "status",
        "total_cost"
    ]

    if not partial:
        for field in required_fields:
            if field not in payload:
                return f"Missing field: {field}"

    allowed_statuses = {"active", "returned", "overdue"}
    if "status" in payload and payload["status"] not in allowed_statuses:
        return "Invalid status. Allowed values: active, returned, overdue"

    return None


@rentals_bp.route("/rentals", methods=["GET"])
def get_all_rentals():
    rentals = []
    for rental in db.rental_data.values():
        customer = db.customer_data.get(rental["customer_id"], {})
        equipment = db.equipment_data.get(rental["equipment_id"], {})

        rentals.append({
            "id": rental["id"],
            "customer_name": customer.get("name", "Unknown Customer"),
            "equipment_name": equipment.get("name", "Unknown Equipment"),
            "equipment_category": equipment.get("category", "Uncategorized"),
            "start_date": rental["start_date"],
            "end_date": rental["end_date"],
            "status": rental["status"].title()
        })
    categories = sorted({rental["equipment_category"] for rental in rentals})
    return render_template("rentals/list.html", rentals=rentals, categories=categories, row_limit=10)


@rentals_bp.route("/rentals/new", methods=["GET", "POST"])
def new_rental():
    if request.method == "POST":
        is_overlap_booking = check_overlap_booking(request.form["equipment_id"], request.form["start_date"], request.form["end_date"])
        if(is_overlap_booking):
            return jsonify({"error": "The selected equipment is already booked for the specified dates."}), 400
        
        total_cost = calculate_total_cost(request.form["equipment_id"], request.form["start_date"], request.form["end_date"])
        db.rental_data[db.next_rental_id] = {
            "id": db.next_rental_id,
            "equipment_id": int(request.form["equipment_id"]),
            "customer_id": int(request.form["customer_id"]),
            "start_date": request.form["start_date"],
            "end_date": request.form["end_date"],
            "status": "Active",
            "total_cost": total_cost
        }
        db.next_rental_id += 1
        return jsonify({"message": "Rental created successfully", "total_cost": total_cost, "is_overlap_booking": is_overlap_booking}), 201
    
    customers = db.customer_data.values()
    equipment = [ eq for eq in db.equipment_data.values() if eq["available"]]
    return render_template("rentals/form.html", customers=customers, equipment=equipment)

@rentals_bp.route("/rentals/<int:rental_id>/return", methods=[ "POST"])
def return_rental(rental_id):
    rental = db.rental_data.get(rental_id)
    if not rental:
        return jsonify({"error": "Rental not found"}), 404
    if rental["status"] != "Active":
        return jsonify({"error": "Only active rentals can be returned"}), 400
    
    rental["status"] = "Returned"
    return jsonify({"message": "Rental returned successfully", "rental": rental}), 200


@rentals_bp.route("/api/rentals", methods=["GET"])
def get_all_rentals_api():
    return jsonify(list(db.rental_data.values())), 200