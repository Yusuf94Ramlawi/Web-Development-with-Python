"""
API routes for TechRent Pro.
RESTful API endpoints for equipment, customers, and rentals.
"""
from flask import Blueprint, jsonify, request
from services import (
  equipment_service,
  customer_service,
  rental_service,
  dashboard_service,
  report_service,
)

api_bp = Blueprint("api", __name__, url_prefix="/api")


def _json_error(message, status_code, errors=None):
  """Return a standardized JSON error payload."""
  payload = {"error": str(message)}
  if errors:
    payload["errors"] = errors
  return jsonify(payload), status_code


def _first_error(errors, fallback="Validation failed"):
    """Extract the first human-readable message from a validation dict."""
    if not errors:
        return fallback
    if isinstance(errors, dict):
        first_value = next(iter(errors.values()))
        return str(first_value)
    return fallback


def _json_payload():
    """Safely parse JSON request payload and return None on invalid/missing body."""
    return request.get_json(silent=True)


# ==================== EQUIPMENT API ====================

@api_bp.route('/equipment', methods=['GET'])
def get_equipment():
    """
    Get all equipment records.

    Args:
        None

    Returns:
        tuple: JSON array of equipment objects and HTTP 200.
    ---
    tags:
      - Equipment
    summary: List equipment
    description: Returns all equipment records.
    responses:
      200:
        description: List of all equipment
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              category:
                type: string
              daily_rate:
                type: number
              quantity:
                type: integer
              description:
                type: string
              available:
                type: boolean
    """
    return jsonify(equipment_service.get_all_equipment()), 200


@api_bp.route('/equipment/available', methods=['GET'])
def get_available_equipment():
    """
    Get all equipment currently available for renting.

    Args:
      None

    Returns:
      tuple: JSON array of available equipment and HTTP 200.
    """
    return jsonify(rental_service.get_available_equipment()), 200


@api_bp.route('/equipment', methods=['POST'])
def create_equipment():
    """
    Create a new equipment record.

    Args:
        None

    Returns:
        tuple: JSON object for created equipment and HTTP 201.
    ---
    tags:
      - Equipment
    summary: Create equipment
    description: Creates an equipment record from a JSON request body.
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - category
            - daily_rate
            - quantity
            - description
          properties:
            name:
              type: string
            category:
              type: string
            daily_rate:
              type: number
            quantity:
              type: integer
            description:
              type: string
            available:
              type: boolean
    responses:
      201:
        description: Equipment created successfully
        schema:
          type: object
      400:
        description: Invalid input
        schema:
          type: object
          properties:
            error:
              type: string
      422:
        description: Write operation failed
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = _json_payload()
    if not data:
        return _json_error("Invalid or missing JSON body", 400)

    errors, validated = equipment_service.validate_equipment_data(
        data,
        for_api=True
    )

    if errors:
      return _json_error(_first_error(errors), 400, errors)

    try:
        equipment = equipment_service.create_equipment(validated)
    except Exception as exc:
        return _json_error(f"Unable to create equipment: {exc}", 422)

    return jsonify(equipment), 201


@api_bp.route('/equipment/<int:equipment_id>', methods=['GET'])
def get_equipment_by_id(equipment_id):
    """
    Get one equipment record by ID.

    Args:
        equipment_id: Equipment identifier.

    Returns:
        tuple: JSON equipment object and HTTP 200, or JSON error and HTTP 404.
    ---
    tags:
      - Equipment
    summary: Get equipment by ID
    description: Returns one equipment record by its ID.
    parameters:
      - in: path
        name: equipment_id
        type: integer
        required: true
    responses:
      200:
        description: Equipment details
        schema:
          type: object
      404:
        description: Equipment not found
        schema:
          type: object
          properties:
            error:
              type: string
    """
    equipment = equipment_service.get_equipment_by_id(equipment_id)
    if not equipment:
        return _json_error("Equipment not found", 404)
    return jsonify(equipment), 200


@api_bp.route('/equipment/<int:equipment_id>', methods=['PUT'])
def update_equipment(equipment_id):
    """
    Update an existing equipment record.

    Args:
        equipment_id: Equipment identifier.

    Returns:
        tuple: JSON updated equipment object and HTTP 200.
    ---
    tags:
      - Equipment
    summary: Update equipment
    description: Updates an equipment record by ID.
    parameters:
      - in: path
        name: equipment_id
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            category:
              type: string
            daily_rate:
              type: number
            quantity:
              type: integer
            description:
              type: string
            available:
              type: boolean
    responses:
      200:
        description: Equipment updated successfully
        schema:
          type: object
      400:
        description: Invalid input
        schema:
          type: object
          properties:
            error:
              type: string
      404:
        description: Equipment not found
        schema:
          type: object
          properties:
            error:
              type: string
      422:
        description: Write operation failed
        schema:
          type: object
          properties:
            error:
              type: string
    """
    equipment = equipment_service.get_equipment_by_id(equipment_id)
    if not equipment:
        return _json_error("Equipment not found", 404)

    data = _json_payload()
    if not data:
        return _json_error("Invalid or missing JSON body", 400)

    update_data = {
        'name': data.get('name', equipment['name']),
        'category': data.get('category', equipment['category']),
        'daily_rate': data.get('daily_rate', equipment['daily_rate']),
        'quantity': data.get('quantity', equipment['quantity']),
        'description': data.get('description', equipment.get('description', '')),
        'available': data.get('available', equipment['available']),
    }

    errors, validated = equipment_service.validate_equipment_data(
        update_data,
        default_daily_rate=equipment['daily_rate'],
        default_quantity=equipment['quantity'],
        for_api=True
    )

    if errors:
      return _json_error(_first_error(errors), 400, errors)

    try:
        updated_equipment = equipment_service.update_equipment(
            equipment_id,
            validated
        )
    except Exception as exc:
        return _json_error(f"Unable to update equipment: {exc}", 422)

    return jsonify(updated_equipment), 200


@api_bp.route('/equipment/<int:equipment_id>', methods=['DELETE'])
def delete_equipment(equipment_id):
    """
    Delete an equipment record.

    Args:
        equipment_id: Equipment identifier.

    Returns:
        tuple: JSON success message and HTTP 200, or JSON error.
    ---
    tags:
      - Equipment
    summary: Delete equipment
    description: Deletes one equipment record by ID.
    parameters:
      - in: path
        name: equipment_id
        type: integer
        required: true
    responses:
      200:
        description: Equipment deleted successfully
        schema:
          type: object
          properties:
            message:
              type: string
      404:
        description: Equipment not found
        schema:
          type: object
          properties:
            error:
              type: string
      422:
        description: Write operation failed
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        deleted = equipment_service.delete_equipment(equipment_id)
    except Exception as exc:
        return _json_error(f"Unable to delete equipment: {exc}", 422)

    if not deleted:
        return _json_error("Equipment not found", 404)

    return jsonify({"message": "Equipment deleted successfully"}), 200


# ==================== CUSTOMERS API ====================

@api_bp.route('/customers', methods=['GET'])
def get_customers():
    """
    Get all customer records.

    Args:
        None

    Returns:
        tuple: JSON array of customers and HTTP 200.
    ---
    tags:
      - Customers
    summary: List customers
    description: Returns all customer records.
    responses:
      200:
        description: List of all customers
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              email:
                type: string
              phone:
                type: string
              created_at:
                type: string
    """
    return jsonify(customer_service.get_all_customers()), 200


@api_bp.route('/customers', methods=['POST'])
def create_customer():
    """
    Create a new customer record.

    Args:
        None

    Returns:
        tuple: JSON created customer object and HTTP 201.
    ---
    tags:
      - Customers
    summary: Create customer
    description: Creates a customer from a JSON request body.
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - email
            - phone
          properties:
            name:
              type: string
            email:
              type: string
            phone:
              type: string
    responses:
      201:
        description: Customer created successfully
        schema:
          type: object
      400:
        description: Invalid input or duplicate email
        schema:
          type: object
          properties:
            error:
              type: string
      422:
        description: Write operation failed
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = _json_payload()
    if not data:
        return _json_error("Invalid or missing JSON body", 400)

    errors = customer_service.validate_customer_data(data, for_api=True)
    if errors:
      return _json_error(_first_error(errors), 400, errors)

    try:
        customer = customer_service.create_customer(
            data.get('name', ''),
            data.get('email', ''),
            data.get('phone', '')
        )
    except Exception as exc:
        return _json_error(f"Unable to create customer: {exc}", 422)

    return jsonify(customer), 201


@api_bp.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer_by_id(customer_id):
    """
    Get one customer record by ID.

    Args:
        customer_id: Customer identifier.

    Returns:
        tuple: JSON customer object and HTTP 200, or JSON error and HTTP 404.
    ---
    tags:
      - Customers
    summary: Get customer by ID
    description: Returns one customer record by ID.
    parameters:
      - in: path
        name: customer_id
        type: integer
        required: true
    responses:
      200:
        description: Customer details
        schema:
          type: object
      404:
        description: Customer not found
        schema:
          type: object
          properties:
            error:
              type: string
    """
    customer = customer_service.get_customer_by_id(customer_id)
    if not customer:
        return _json_error("Customer not found", 404)
    return jsonify(customer), 200


@api_bp.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    """
    Update a customer record.

    Args:
        customer_id: Customer identifier.

    Returns:
        tuple: JSON updated customer object and HTTP 200.
    ---
    tags:
      - Customers
    summary: Update customer
    description: Updates a customer by ID.
    parameters:
      - in: path
        name: customer_id
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            email:
              type: string
            phone:
              type: string
    responses:
      200:
        description: Customer updated successfully
        schema:
          type: object
      400:
        description: Invalid input or duplicate email
        schema:
          type: object
          properties:
            error:
              type: string
      404:
        description: Customer not found
        schema:
          type: object
          properties:
            error:
              type: string
      422:
        description: Write operation failed
        schema:
          type: object
          properties:
            error:
              type: string
    """
    customer = customer_service.get_customer_by_id(customer_id)
    if not customer:
        return _json_error("Customer not found", 404)

    data = _json_payload()
    if not data:
        return _json_error("Invalid or missing JSON body", 400)

    update_data = {
        'name': data.get('name', customer['name']),
        'email': data.get('email', customer['email']),
        'phone': data.get('phone', customer['phone']),
    }

    errors = customer_service.validate_customer_data(
        update_data,
        customer_id=customer_id,
        for_api=True
    )

    if errors:
      return _json_error(_first_error(errors), 400, errors)

    try:
        updated_customer = customer_service.update_customer(
            customer_id,
            update_data['name'],
            update_data['email'],
            update_data['phone']
        )
    except Exception as exc:
        return _json_error(f"Unable to update customer: {exc}", 422)

    return jsonify(updated_customer), 200


@api_bp.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    """
    Delete a customer record.

    Args:
        customer_id: Customer identifier.

    Returns:
        tuple: JSON success message and HTTP 200, or JSON error body.
    ---
    tags:
      - Customers
    summary: Delete customer
    description: Deletes a customer by ID.
    parameters:
      - in: path
        name: customer_id
        type: integer
        required: true
    responses:
      200:
        description: Customer deleted successfully
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Customer has active rentals
        schema:
          type: object
          properties:
            error:
              type: string
      404:
        description: Customer not found
        schema:
          type: object
          properties:
            error:
              type: string
      422:
        description: Write operation failed
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        success, message = customer_service.delete_customer(customer_id)
    except Exception as exc:
        return _json_error(f"Unable to delete customer: {exc}", 422)

    if not success:
        status_code = 404 if "not found" in message.lower() else 400
        return _json_error(message, status_code)

    return jsonify({"message": message}), 200


# ==================== RENTALS API ====================

@api_bp.route('/rentals', methods=['GET'])
def get_rentals():
    """
    Get all rental records.

    Args:
        None

    Returns:
        tuple: JSON array of rentals and HTTP 200.
    ---
    tags:
      - Rentals
    summary: List rentals
    description: Returns all rentals.
    responses:
      200:
        description: List of all rentals
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              equipment_id:
                type: integer
              customer_id:
                type: integer
              start_date:
                type: string
              end_date:
                type: string
              status:
                type: string
              total_cost:
                type: number
    """
    return jsonify(rental_service.get_all_rentals_view()), 200


@api_bp.route('/rentals', methods=['POST'])
def create_rental():
    """
    Create a new rental record.

    Args:
        None

    Returns:
        tuple: JSON created rental object and HTTP 201.
    ---
    tags:
      - Rentals
    summary: Create rental
    description: Creates a rental from a JSON request body.
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - equipment_id
            - customer_id
            - start_date
            - end_date
          properties:
            equipment_id:
              type: integer
            customer_id:
              type: integer
            start_date:
              type: string
              format: date
            end_date:
              type: string
              format: date
    responses:
      201:
        description: Rental created successfully
        schema:
          type: object
      400:
        description: Invalid input or unavailable equipment
        schema:
          type: object
          properties:
            error:
              type: string
      422:
        description: Write operation failed
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = _json_payload()
    if not data:
        return _json_error("Invalid or missing JSON body", 400)

    errors, validated = rental_service.validate_rental_data(data, for_api=True)
    if errors:
      return _json_error(_first_error(errors), 400, errors)

    if rental_service.check_overlap_booking(
        validated['equipment_id'],
        validated['start_date'],
        validated['end_date']
    ):
        return _json_error(
            "The selected equipment is already booked for the specified dates.",
            400
        )

    try:
        rental = rental_service.create_rental(
            validated['equipment_id'],
            validated['customer_id'],
            validated['start_date'],
            validated['end_date']
        )
    except Exception as exc:
        return _json_error(f"Unable to create rental: {exc}", 422)

    return jsonify(rental), 201


@api_bp.route('/rentals/<int:rental_id>', methods=['GET'])
def get_rental_by_id(rental_id):
    """
    Get one rental record by ID.

    Args:
        rental_id: Rental identifier.

    Returns:
        tuple: JSON rental object and HTTP 200, or JSON error and HTTP 404.
    ---
    tags:
      - Rentals
    summary: Get rental by ID
    description: Returns one rental record by its ID.
    parameters:
      - in: path
        name: rental_id
        type: integer
        required: true
    responses:
      200:
        description: Rental details
        schema:
          type: object
      404:
        description: Rental not found
        schema:
          type: object
          properties:
            error:
              type: string
    """
    rental = rental_service.get_rental_by_id(rental_id)
    if not rental:
        return _json_error("Rental not found", 404)
    return jsonify(rental), 200


@api_bp.route('/rentals/<int:rental_id>', methods=['PUT'])
def update_rental(rental_id):
    """
    Update an existing rental record.

    Args:
      rental_id: Rental identifier.

    Returns:
      tuple: JSON updated rental object and HTTP 200.
    """
    existing_rental = rental_service.get_rental_by_id(rental_id)
    if not existing_rental:
        return _json_error("Rental not found", 404)

    data = _json_payload()
    if not data:
        return _json_error("Invalid or missing JSON body", 400)

    update_data = {
        "equipment_id": data.get("equipment_id", existing_rental["equipment_id"]),
        "customer_id": data.get("customer_id", existing_rental["customer_id"]),
        "start_date": data.get("start_date", existing_rental["start_date"]),
        "end_date": data.get("end_date", existing_rental["end_date"]),
        "status": data.get("status", existing_rental.get("status", "active")),
    }

    errors, validated = rental_service.validate_rental_data(
        update_data,
        for_api=True,
    )
    if errors:
        return _json_error(_first_error(errors), 400, errors)

    if rental_service.check_overlap_booking(
        validated["equipment_id"],
        validated["start_date"],
        validated["end_date"],
        exclude_rental_id=rental_id,
    ):
        overlap_errors = {
            "date_range": (
                "The selected equipment is already booked for "
                "the specified dates."
            )
        }
        return _json_error(_first_error(overlap_errors), 400, overlap_errors)

    try:
        rental = rental_service.update_rental(
            rental_id,
            validated["equipment_id"],
            validated["customer_id"],
            validated["start_date"],
            validated["end_date"],
            validated["status"],
        )
    except Exception as exc:
        return _json_error(f"Unable to update rental: {exc}", 422)

    return jsonify(rental), 200


@api_bp.route('/rentals/<int:rental_id>', methods=['DELETE'])
def delete_rental(rental_id):
    """
    Delete a rental record.

    Args:
      rental_id: Rental identifier.

    Returns:
      tuple: JSON success message and HTTP 200, or JSON error body.
    """
    try:
        deleted = rental_service.delete_rental(rental_id)
    except Exception as exc:
        return _json_error(f"Unable to delete rental: {exc}", 422)

    if not deleted:
        return _json_error("Rental not found", 404)

    return jsonify({"message": "Rental deleted successfully"}), 200


@api_bp.route('/rentals/<int:rental_id>/return', methods=['PUT'])
def return_rental(rental_id):
    """
    Mark a rental as returned.

    Args:
        rental_id: Rental identifier.

    Returns:
        tuple: JSON updated rental object and HTTP 200, or JSON error body.
    ---
    tags:
      - Rentals
    summary: Return rental
    description: Marks the rental status as returned.
    parameters:
      - in: path
        name: rental_id
        type: integer
        required: true
    responses:
      200:
        description: Rental marked as returned
        schema:
          type: object
      404:
        description: Rental not found
        schema:
          type: object
          properties:
            error:
              type: string
      422:
        description: Write operation failed
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        rental = rental_service.update_rental_status(rental_id, 'returned')
    except Exception as exc:
        return _json_error(f"Unable to update rental status: {exc}", 422)

    if not rental:
        return _json_error("Rental not found", 404)

    return jsonify(rental), 200


@api_bp.route('/dashboard/summary', methods=['GET'])
def get_dashboard_summary():
    """
    Get dashboard counters and recent-rental data.

    Returns:
      tuple: JSON dashboard summary and HTTP 200.
    """
    return jsonify(dashboard_service.get_dashboard_summary()), 200


@api_bp.route('/reports/summary', methods=['GET'])
def get_reports_summary():
    """
    Get reports analytics summary.

    Returns:
      tuple: JSON reports summary and HTTP 200.
    """
    return jsonify(report_service.get_reports_summary()), 200
