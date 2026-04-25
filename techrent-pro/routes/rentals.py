import db
from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from utils.pagination import Paginator
from services import rental_service

rentals_bp = Blueprint("rentals", __name__)


@rentals_bp.route("/rentals", methods=["GET"])
def get_all_rentals():
    selected_category = request.args.get("category", "").strip()
    selected_status = request.args.get("status", "").strip().lower()
    search_query = request.args.get("q", "").strip()

    rentals = [
        rental_service.build_rental_view(rental)
        for rental in rental_service.get_all_rentals()
    ]

    categories = sorted({rental["equipment_category"] for rental in rentals})
    statuses = ["active", "returned", "overdue"]

    if selected_category:
        rentals = [
            rental
            for rental in rentals
            if rental["equipment_category"].lower() == selected_category.lower()
        ]

    if selected_status:
        rentals = [
            rental
            for rental in rentals
            if rental["status"].lower() == selected_status
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

    pager = Paginator()
    result = pager.paginate(rentals)
    return render_template(
        "rentals/list.html",
        rentals=result['data'],
        categories=categories,
        statuses=statuses,
        selected_category=selected_category,
        selected_status=selected_status,
        search_query=search_query,
        pagination=result['pagination'],
    )


@rentals_bp.route("/rentals/new", methods=["GET", "POST"])
def new_rental():
    if request.method == "POST":
        equipment_id = request.form["equipment_id"]
        customer_id = request.form["customer_id"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        if rental_service.check_overlap_booking(
            equipment_id, start_date, end_date
        ):
            customers = list(db.customer_data.values())
            equipment = rental_service.get_available_equipment()
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

        rental_service.create_rental(
            equipment_id, customer_id, start_date, end_date
        )
        return redirect(url_for("rentals.get_all_rentals"))

    customers = list(db.customer_data.values())
    equipment = rental_service.get_available_equipment()
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
    rental = rental_service.get_rental_by_id(rental_id)
    if not rental:
        return redirect(url_for("rentals.get_all_rentals"))

    return render_template(
        "rentals/detail.html",
        rental=rental_service.build_rental_view(rental)
    )


@rentals_bp.route("/rentals/<int:rental_id>/edit", methods=["GET", "POST"])
def edit_rental(rental_id):
    rental = rental_service.get_rental_by_id(rental_id)
    if not rental:
        return redirect(url_for("rentals.get_all_rentals"))

    if request.method == "POST":
        equipment_id = request.form["equipment_id"]
        customer_id = request.form["customer_id"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        status = request.form.get("status", "active").strip().lower()

        if rental_service.check_overlap_booking(
            equipment_id, start_date, end_date, exclude_rental_id=rental_id
        ):
            customers = list(db.customer_data.values())
            equipment = list(db.equipment_data.values())
            return (
                render_template(
                    "rentals/form.html",
                    customers=customers,
                    equipment=equipment,
                    rental=request.form,
                    form_action=url_for(
                        "rentals.edit_rental", rental_id=rental_id
                    ),
                    submit_label="Save changes",
                    error_message="The selected equipment is already booked for the specified dates.",
                ),
                400,
            )

        rental_service.update_rental(
            rental_id, equipment_id, customer_id, start_date, end_date, status
        )
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
    rental_service.get_rental_by_id(rental_id)  # Check existence
    db.rental_data.pop(rental_id, None)
    return redirect(url_for("rentals.get_all_rentals"))


@rentals_bp.route("/rentals/<int:rental_id>/return", methods=["POST"])
def return_rental(rental_id):
    rental = rental_service.get_rental_by_id(rental_id)
    if not rental:
        return redirect(url_for("rentals.get_all_rentals"))
    if str(rental.get("status", "")).lower() != "active":
        return redirect(url_for("rentals.get_all_rentals"))

    rental_service.update_rental_status(rental_id, "returned")
    return redirect(url_for("rentals.get_all_rentals"))


@rentals_bp.route("/api/rentals", methods=["GET"])
def get_all_rentals_api():
    return jsonify(rental_service.get_all_rentals()), 200
