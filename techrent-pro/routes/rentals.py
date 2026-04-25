import datetime
import db
from flask import Blueprint, jsonify, redirect, render_template, request, url_for

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


def check_overlap_booking(equipment_id, start_date, end_date, exclude_rental_id=None):
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    for rental in db.rental_data.values():
        if exclude_rental_id is not None and rental["id"] == exclude_rental_id:
            continue

        if (
            rental["equipment_id"] == int(equipment_id)
            and str(rental.get("status", "")).lower() == "active"
        ):
            existing_start = datetime.datetime.strptime(rental["start_date"], "%Y-%m-%d")
            existing_end = datetime.datetime.strptime(rental["end_date"], "%Y-%m-%d")

            if start <= existing_end and end >= existing_start:
                return True

    return False


def build_rental_view(rental):
    customer = db.customer_data.get(rental["customer_id"], {})
    equipment = db.equipment_data.get(rental["equipment_id"], {})
    return {
        "id": rental["id"],
        "customer_id": rental["customer_id"],
        "equipment_id": rental["equipment_id"],
        "customer_name": customer.get("name", "Unknown Customer"),
        "equipment_name": equipment.get("name", "Unknown Equipment"),
        "equipment_category": equipment.get("category", "Uncategorized"),
        "start_date": rental["start_date"],
        "end_date": rental["end_date"],
        "status": str(rental.get("status", "")).title(),
        "total_cost": rental.get("total_cost", 0.0),
    }

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
    selected_category = request.args.get("category", "").strip()
    search_query = request.args.get("q", "").strip()

    rentals = [build_rental_view(rental) for rental in db.rental_data.values()]

    categories = sorted({rental["equipment_category"] for rental in rentals})

    if selected_category:
        rentals = [
            rental
            for rental in rentals
            if rental["equipment_category"].lower() == selected_category.lower()
        ]

    if search_query:
        query_lower = search_query.lower()
        rentals = [
            rental
            for rental in rentals
            if query_lower in str(rental["id"]).lower()
            or query_lower in rental["customer_name"].lower()
            or query_lower in rental["equipment_name"].lower()
            or query_lower in rental["equipment_category"].lower()
        ]

    return render_template(
        "rentals/list.html",
        rentals=rentals,
        categories=categories,
        selected_category=selected_category,
        search_query=search_query,
        row_limit=10,
    )


@rentals_bp.route("/rentals/new", methods=["GET", "POST"])
def new_rental():
    if request.method == "POST":
        equipment_id = request.form["equipment_id"]
        customer_id = request.form["customer_id"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        status = request.form.get("status", "active").strip().lower()

        if check_overlap_booking(equipment_id, start_date, end_date):
            customers = list(db.customer_data.values())
            equipment = [eq for eq in db.equipment_data.values() if eq["available"]]
            return (
                render_template(
                    "rentals/form.html",
                    customers=customers,
                    equipment=equipment,
                    rental=request.form,
                    form_action=url_for("rentals.new_rental"),
                    submit_label="Add rental",
                    error_message="The selected equipment is already booked for the specified dates.",
                ),
                400,
            )

        total_cost = calculate_total_cost(equipment_id, start_date, end_date)
        db.rental_data[db.next_rental_id] = {
            "id": db.next_rental_id,
            "equipment_id": int(equipment_id),
            "customer_id": int(customer_id),
            "start_date": start_date,
            "end_date": end_date,
            "status": status if status in {"active", "returned", "overdue"} else "active",
            "total_cost": total_cost,
        }
        db.next_rental_id += 1
        return redirect(url_for("rentals.get_all_rentals"))

    customers = list(db.customer_data.values())
    equipment = [eq for eq in db.equipment_data.values() if eq["available"]]
    return render_template(
        "rentals/form.html",
        customers=customers,
        equipment=equipment,
        rental=None,
        form_action=url_for("rentals.new_rental"),
        submit_label="Add rental",
    )


@rentals_bp.route("/rentals/<int:rental_id>", methods=["GET"])
def view_rental(rental_id):
    rental = db.rental_data.get(rental_id)
    if not rental:
        return redirect(url_for("rentals.get_all_rentals"))

    return render_template("rentals/detail.html", rental=build_rental_view(rental))


@rentals_bp.route("/rentals/<int:rental_id>/edit", methods=["GET", "POST"])
def edit_rental(rental_id):
    rental = db.rental_data.get(rental_id)
    if not rental:
        return redirect(url_for("rentals.get_all_rentals"))

    if request.method == "POST":
        equipment_id = request.form["equipment_id"]
        customer_id = request.form["customer_id"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        status = request.form.get("status", "active").strip().lower()

        if check_overlap_booking(equipment_id, start_date, end_date, exclude_rental_id=rental_id):
            customers = list(db.customer_data.values())
            equipment = list(db.equipment_data.values())
            return (
                render_template(
                    "rentals/form.html",
                    customers=customers,
                    equipment=equipment,
                    rental=request.form,
                    form_action=url_for("rentals.edit_rental", rental_id=rental_id),
                    submit_label="Save changes",
                    error_message="The selected equipment is already booked for the specified dates.",
                ),
                400,
            )

        rental["equipment_id"] = int(equipment_id)
        rental["customer_id"] = int(customer_id)
        rental["start_date"] = start_date
        rental["end_date"] = end_date
        rental["status"] = status if status in {"active", "returned", "overdue"} else "active"
        rental["total_cost"] = calculate_total_cost(equipment_id, start_date, end_date)
        return redirect(url_for("rentals.get_all_rentals"))

    customers = list(db.customer_data.values())
    equipment = list(db.equipment_data.values())
    return render_template(
        "rentals/form.html",
        customers=customers,
        equipment=equipment,
        rental=rental,
        form_action=url_for("rentals.edit_rental", rental_id=rental_id),
        submit_label="Save changes",
    )


@rentals_bp.route("/rentals/<int:rental_id>/delete", methods=["POST"])
def delete_rental(rental_id):
    db.rental_data.pop(rental_id, None)
    return redirect(url_for("rentals.get_all_rentals"))

@rentals_bp.route("/rentals/<int:rental_id>/return", methods=[ "POST"])
def return_rental(rental_id):
    rental = db.rental_data.get(rental_id)
    if not rental:
        return jsonify({"error": "Rental not found"}), 404
    if str(rental.get("status", "")).lower() != "active":
        return jsonify({"error": "Only active rentals can be returned"}), 400

    rental["status"] = "returned"
    return jsonify({"message": "Rental returned successfully", "rental": rental}), 200


@rentals_bp.route("/api/rentals", methods=["GET"])
def get_all_rentals_api():
    return jsonify(list(db.rental_data.values())), 200