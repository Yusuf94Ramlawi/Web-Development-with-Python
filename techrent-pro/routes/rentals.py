from flask import Blueprint, redirect, render_template, request, url_for, flash
from utils.pagination import Paginator
from services import frontend_api_service

rentals_bp = Blueprint("rentals", __name__)


def _load_rental_form_data(include_all_equipment=False):
    """Fetch customers and equipment options for rental form pages via API."""
    customers_status, customers_payload = frontend_api_service.get(
        '/api/customers')
    customers = (
        customers_payload
        if customers_status == 200 and isinstance(customers_payload, list)
        else []
    )

    equipment_path = '/api/equipment' if include_all_equipment else '/api/equipment/available'
    equipment_status, equipment_payload = frontend_api_service.get(
        equipment_path)
    equipment = (
        equipment_payload
        if equipment_status == 200 and isinstance(equipment_payload, list)
        else []
    )

    return customers, equipment


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

    status_code, payload = frontend_api_service.get('/api/rentals')
    rentals = payload if status_code == 200 and isinstance(
        payload, list) else []

    if status_code != 200:
        flash('Unable to load rentals from API.', 'danger')

    statuses = ["active", "returned", "overdue"]

    if selected_status:
        rentals = [
            rental
            for rental in rentals
            if rental.get("status", "").lower() == selected_status
        ]

    if search_query:
        query_lower = search_query.lower()
        rentals = [
            rental
            for rental in rentals
            if query_lower in rental.get("customer_name", "").lower()
            or query_lower in rental.get("equipment_name", "").lower()
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

        create_status, payload = frontend_api_service.post(
            '/api/rentals',
            json_data=form_data,
        )
        if create_status != 201:
            customers, equipment = _load_rental_form_data(
                include_all_equipment=False)
            errors = frontend_api_service.extract_errors(payload)
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

        return redirect(url_for("rentals.get_all_rentals"))

    customers, equipment = _load_rental_form_data(include_all_equipment=False)
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
    status_code, rental = frontend_api_service.get(f'/api/rentals/{rental_id}')
    if status_code != 200:
        return redirect(url_for("rentals.get_all_rentals"))

    return redirect(url_for("rentals.get_all_rentals"))


@rentals_bp.route("/rentals/<int:rental_id>/edit", methods=["GET", "POST"])
def edit_rental(rental_id):
    """
    Edit an existing rental.

    Args:
        rental_id: Rental identifier.

    Returns:
        Response: Rental form or redirect to rental list on success.
    """
    rental_status, rental = frontend_api_service.get(
        f'/api/rentals/{rental_id}')
    if rental_status != 200:
        return redirect(url_for("rentals.get_all_rentals"))

    if request.method == "POST":
        form_data = {
            "equipment_id": request.form.get("equipment_id", "").strip(),
            "customer_id": request.form.get("customer_id", "").strip(),
            "start_date": request.form.get("start_date", "").strip(),
            "end_date": request.form.get("end_date", "").strip(),
            "status": request.form.get("status", "active").strip().lower(),
        }

        update_status, payload = frontend_api_service.put(
            f'/api/rentals/{rental_id}',
            json_data=form_data,
        )
        if update_status != 200:
            customers, equipment = _load_rental_form_data(
                include_all_equipment=True)
            errors = frontend_api_service.extract_errors(payload)
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

        return redirect(url_for("rentals.get_all_rentals"))

    customers, equipment = _load_rental_form_data(include_all_equipment=True)
    return render_template(
        "rentals/form.html",
        customers=customers,
        equipment=equipment,
        rental=rental,
        form_action=url_for("rentals.edit_rental", rental_id=rental_id),
        submit_label="Save changes",
        errors={},
    )


@rentals_bp.route("/rentals/<int:rental_id>/return", methods=["POST"])
def return_rental(rental_id):
    """
    Mark an active rental as returned.

    Args:
        rental_id: Rental identifier.

    Returns:
        Response: Redirect to rental list.
    """
    status_code, payload = frontend_api_service.put(
        f'/api/rentals/{rental_id}/return')
    if status_code != 200:
        flash(payload.get('error', 'Unable to return rental'), 'danger')
    return redirect(url_for("rentals.get_all_rentals"))
