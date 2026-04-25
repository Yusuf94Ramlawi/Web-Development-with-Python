"""
API routes for TechRent Pro
RESTful API endpoints for equipment, customers, and rentals
"""
import db
from flask import Blueprint, jsonify, request
from datetime import datetime
import re
from services import equipment_service, customer_service, rental_service

api_bp = Blueprint("api", __name__, url_prefix="/api")


# ==================== EQUIPMENT API ====================

@api_bp.route('/equipment', methods=['GET'])
def get_equipment():
    """
    Get all equipment
    ---
    tags:
      - Equipment
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


@api_bp.route('/equipment', methods=['POST'])
def create_equipment():
    """
    Create new equipment
    ---
    tags:
      - Equipment
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
      400:
        description: Invalid input
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Validate using service layer
    errors, validated = equipment_service.validate_equipment_data(
        data,
        for_api=True
    )

    if errors:
        return jsonify({"errors": errors}), 400

    # Create equipment using service layer
    equipment = equipment_service.create_equipment(validated)
    return jsonify(equipment), 201


@api_bp.route('/equipment/<int:equipment_id>', methods=['GET'])
def get_equipment_by_id(equipment_id):
    """
    Get equipment by ID
    ---
    tags:
      - Equipment
    parameters:
      - in: path
        name: equipment_id
        type: integer
        required: true
    responses:
      200:
        description: Equipment details
      404:
        description: Equipment not found
    """
    equipment = equipment_service.get_equipment_by_id(equipment_id)
    if not equipment:
        return jsonify({"error": "Equipment not found"}), 404
    return jsonify(equipment), 200


@api_bp.route('/equipment/<int:equipment_id>', methods=['PUT'])
def update_equipment(equipment_id):
    """
    Update equipment
    ---
    tags:
      - Equipment
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
      404:
        description: Equipment not found
    """
    equipment = equipment_service.get_equipment_by_id(equipment_id)
    if not equipment:
        return jsonify({"error": "Equipment not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Merge with existing data for partial updates
    update_data = {
        'name': data.get('name', equipment['name']),
        'category': data.get('category', equipment['category']),
        'daily_rate': data.get('daily_rate', equipment['daily_rate']),
        'quantity': data.get('quantity', equipment['quantity']),
        'description': data.get(
            'description', equipment.get('description', '')
        ),
        'available': data.get('available', equipment['available']),
    }

    # Validate using service layer
    errors, validated = equipment_service.validate_equipment_data(
        update_data,
        default_daily_rate=equipment['daily_rate'],
        default_quantity=equipment['quantity'],
        for_api=True
    )

    if errors:
        return jsonify({"errors": errors}), 400

    # Update equipment using service layer
    updated_equipment = equipment_service.update_equipment(
        equipment_id, validated
    )
    return jsonify(updated_equipment), 200


@api_bp.route('/equipment/<int:equipment_id>', methods=['DELETE'])
def delete_equipment(equipment_id):
    """
    Delete equipment
    ---
    tags:
      - Equipment
    parameters:
      - in: path
        name: equipment_id
        type: integer
        required: true
    responses:
      200:
        description: Equipment deleted successfully
      404:
        description: Equipment not found
    """
    if not equipment_service.delete_equipment(equipment_id):
        return jsonify({"error": "Equipment not found"}), 404

    return jsonify({"message": "Equipment deleted successfully"}), 200


# ==================== CUSTOMERS API ====================

@api_bp.route('/customers', methods=['GET'])
def get_customers():
    """
    Get all customers
    ---
    tags:
      - Customers
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
    Create new customer
    ---
    tags:
      - Customers
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
      400:
        description: Invalid input or duplicate email
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Validate using service layer
    errors = customer_service.validate_customer_data(data, for_api=True)
    if errors:
        return jsonify({"errors": errors}), 400

    # Create customer using service layer
    customer = customer_service.create_customer(
        data.get('name', ''),
        data.get('email', ''),
        data.get('phone', '')
    )
    return jsonify(customer), 201


@api_bp.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer_by_id(customer_id):
    """
    Get customer by ID
    ---
    tags:
      - Customers
    parameters:
      - in: path
        name: customer_id
        type: integer
        required: true
    responses:
      200:
        description: Customer details
      404:
        description: Customer not found
    """
    customer = customer_service.get_customer_by_id(customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify(customer), 200


@api_bp.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    """
    Update customer
    ---
    tags:
      - Customers
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
      400:
        description: Invalid input or duplicate email
      404:
        description: Customer not found
    """
    customer = customer_service.get_customer_by_id(customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Merge with existing data for partial updates
    update_data = {
        'name': data.get('name', customer['name']),
        'email': data.get('email', customer['email']),
        'phone': data.get('phone', customer['phone']),
    }

    # Validate using service layer
    errors = customer_service.validate_customer_data(
        update_data,
        customer_id=customer_id,
        for_api=True
    )

    if errors:
        return jsonify({"errors": errors}), 400

    # Update customer using service layer
    updated_customer = customer_service.update_customer(
        customer_id,
        update_data['name'],
        update_data['email'],
        update_data['phone']
    )
    return jsonify(updated_customer), 200


@api_bp.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    """
    Delete customer
    ---
    tags:
      - Customers
    parameters:
      - in: path
        name: customer_id
        type: integer
        required: true
    responses:
      200:
        description: Customer deleted successfully
      400:
        description: Customer has active rentals
      404:
        description: Customer not found
    """
    success, message = customer_service.delete_customer(customer_id)

    if not success:
        status_code = 404 if "not found" in message.lower() else 400
        return jsonify({"error": message}), status_code

    return jsonify({"message": message}), 200


# ==================== RENTALS API ====================

@api_bp.route('/rentals', methods=['GET'])
def get_rentals():
    """
    Get all rentals
    ---
    tags:
      - Rentals
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
    return jsonify(list(db.rental_data.values())), 200


@api_bp.route('/rentals', methods=['POST'])
def create_rental():
    """
    Create new rental
    ---
    tags:
      - Rentals
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
      400:
        description: Invalid input or equipment unavailable
      404:
        description: Equipment or customer not found
    """
    data = request.get_json()
    required = ['equipment_id', 'customer_id', 'start_date', 'end_date']
    if not data or not all(k in data for k in required):
        return jsonify({"error": "Missing required fields"}), 400

    equipment_id = int(data['equipment_id'])
    customer_id = int(data['customer_id'])

    # Validate equipment and customer exist
    if equipment_id not in db.equipment_data:
        return jsonify({"error": "Equipment not found"}), 404
    if customer_id not in db.customer_data:
        return jsonify({"error": "Customer not found"}), 404

    equipment = db.equipment_data[equipment_id]

    # Calculate total cost
    try:
        start = datetime.strptime(data['start_date'], "%Y-%m-%d")
        end = datetime.strptime(data['end_date'], "%Y-%m-%d")
        days = (end - start).days + 1
        if days <= 0:
            return jsonify({"error": "Invalid date range"}), 400
        total_cost = round(equipment['daily_rate'] * days, 2)
    except ValueError:
        return jsonify({
            "error": "Invalid date format. Use YYYY-MM-DD"
        }), 400

    new_id = db.next_rental_id
    db.rental_data[new_id] = {
        "id": new_id,
        "equipment_id": equipment_id,
        "customer_id": customer_id,
        "start_date": data['start_date'],
        "end_date": data['end_date'],
        "status": "active",
        "total_cost": total_cost,
    }
    db.next_rental_id += 1
    return jsonify(db.rental_data[new_id]), 201


@api_bp.route('/rentals/<int:rental_id>', methods=['GET'])
def get_rental_by_id(rental_id):
    """
    Get rental by ID
    ---
    tags:
      - Rentals
    parameters:
      - in: path
        name: rental_id
        type: integer
        required: true
    responses:
      200:
        description: Rental details
      404:
        description: Rental not found
    """
    rental = db.rental_data.get(rental_id)
    if not rental:
        return jsonify({"error": "Rental not found"}), 404
    return jsonify(rental), 200


@api_bp.route('/rentals/<int:rental_id>/return', methods=['PUT'])
def return_rental(rental_id):
    """
    Mark rental as returned
    ---
    tags:
      - Rentals
    parameters:
      - in: path
        name: rental_id
        type: integer
        required: true
    responses:
      200:
        description: Rental marked as returned
      404:
        description: Rental not found
    """
    rental = db.rental_data.get(rental_id)
    if not rental:
        return jsonify({"error": "Rental not found"}), 404

    rental['status'] = 'returned'
    return jsonify(rental), 200
