import db
from flask import Blueprint, redirect, render_template, request, url_for
from utils.pagination import Paginator
from services import rental_service

rentals_bp = Blueprint("rentals", __name__)


@rentals_bp.route("/rentals", methods=["GET"])
def get_all_rentals():
    """
    List rentals with optional status/search filtering and pagination.

    Args:
        None

    Returns:
        Response: Rendered rentals list page.
    """
    selected_status = request.args.get("status", "").strip().lower()
    search_query = request.args.get("q", "").strip()

    rentals = [
        rental_service.build_rental_view(rental)
        for rental in rental_service.get_all_rentals()
    ]

    statuses = ["active", "returned", "overdue"]

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
            if query_lower in rental["customer_name"].lower()
            or query_lower in rental["equipment_name"].lower()
        ]

    pager = Paginator()
    result = pager.paginate(rentals)
    return render_template(
        "rentals/list.html",
        rentals=result['data'],
        statuses=statuses,
        selected_status=selected_status,
        search_query=search_query,
        pagination=result['pagination'],
    )


@rentals_bp.route("/rentals/new", methods=["GET", "POST"])
def new_rental():
    """
    Create a new rental from form input.

    Args:
        None

    Returns:
        Response: Rental form or redirect to rental list on success.
    """
    if request.method == "POST":
        form_data = {
            "equipment_id": request.form.get("equipment_id", "").strip(),
            "customer_id": request.form.get("customer_id", "").strip(),
            "start_date": request.form.get("start_date", "").strip(),
            "end_date": request.form.get("end_date", "").strip(),
        }

        errors, validated = rental_service.validate_rental_data(form_data)
        if errors:
            customers = list(db.customer_data.values())
            equipment = rental_service.get_available_equipment()
            return (
                render_template(
                    "rentals/form.html",
                    customers=customers,
                    equipment=equipment,
                    rental=form_data,
                    form_action=url_for("rentals.new_rental"),
                    submit_label="Add rental",
                    errors=errors,
                ),
                400,
            )

        equipment_id = validated["equipment_id"]
        customer_id = validated["customer_id"]
        start_date = validated["start_date"]
        end_date = validated["end_date"]

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
                    rental=form_data,
                    form_action=url_for("rentals.new_rental"),
                    submit_label="Add rental",
                    errors={
                        "date_range": (
                            "The selected equipment is already booked for "
                            "the specified dates."
                        )
                    },
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
        errors={},
    )


@rentals_bp.route("/rentals/<int:rental_id>", methods=["GET"])
def view_rental(rental_id):
    """
    View details for one rental.

    Args:
        rental_id: Rental identifier.

    Returns:
        Response: Rendered rental details or redirect when missing.
    """
    rental = rental_service.get_rental_by_id(rental_id)
    if not rental:
        return redirect(url_for("rentals.get_all_rentals"))

    return render_template(
        "rentals/detail.html",
        rental=rental_service.build_rental_view(rental)
    )


@rentals_bp.route("/rentals/<int:rental_id>/edit", methods=["GET", "POST"])
def edit_rental(rental_id):
    """
    Edit an existing rental.

    Args:
        rental_id: Rental identifier.

    Returns:
        Response: Rental form or redirect to rental list on success.
    """
    rental = rental_service.get_rental_by_id(rental_id)
    if not rental:
        return redirect(url_for("rentals.get_all_rentals"))

    if request.method == "POST":
        form_data = {
            "equipment_id": request.form.get("equipment_id", "").strip(),
            "customer_id": request.form.get("customer_id", "").strip(),
            "start_date": request.form.get("start_date", "").strip(),
            "end_date": request.form.get("end_date", "").strip(),
            "status": request.form.get("status", "active").strip().lower(),
        }

        errors, validated = rental_service.validate_rental_data(form_data)
        if errors:
            customers = list(db.customer_data.values())
            equipment = list(db.equipment_data.values())
            return (
                render_template(
                    "rentals/form.html",
                    customers=customers,
                    equipment=equipment,
                    rental=form_data,
                    form_action=url_for(
                        "rentals.edit_rental", rental_id=rental_id
                    ),
                    submit_label="Save changes",
                    errors=errors,
                ),
                400,
            )

        equipment_id = validated["equipment_id"]
        customer_id = validated["customer_id"]
        start_date = validated["start_date"]
        end_date = validated["end_date"]
        status = validated["status"]

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
                    rental=form_data,
                    form_action=url_for(
                        "rentals.edit_rental", rental_id=rental_id
                    ),
                    submit_label="Save changes",
                    errors={
                        "date_range": (
                            "The selected equipment is already booked for "
                            "the specified dates."
                        )
                    },
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
        errors={},
    )


@rentals_bp.route("/rentals/<int:rental_id>/delete", methods=["POST"])
def delete_rental(rental_id):
    """
    Delete a rental.

    Args:
        rental_id: Rental identifier.

    Returns:
        Response: Redirect to rental list.
    """
    rental_service.get_rental_by_id(rental_id)  # Check existence
    db.rental_data.pop(rental_id, None)
    return redirect(url_for("rentals.get_all_rentals"))


@rentals_bp.route("/rentals/<int:rental_id>/return", methods=["POST"])
def return_rental(rental_id):
    """
    Mark an active rental as returned.

    Args:
        rental_id: Rental identifier.

    Returns:
        Response: Redirect to rental list.
    """
    rental = rental_service.get_rental_by_id(rental_id)
    if not rental:
        return redirect(url_for("rentals.get_all_rentals"))
    if str(rental.get("status", "")).lower() != "active":
        return redirect(url_for("rentals.get_all_rentals"))

    rental_service.update_rental_status(rental_id, "returned")
    return redirect(url_for("rentals.get_all_rentals"))

