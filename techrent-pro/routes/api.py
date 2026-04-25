"""
API routes for TechRent Pro
RESTful API endpoints for equipment, customers, and rentals
"""
import db
from flask import Blueprint, jsonify, request
from datetime import datetime
import re

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
    return jsonify(list(db.equipment_data.values())), 200


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
    if not data or not all(k in data for k in ['name', 'category', 'daily_rate', 'quantity']):
        return jsonify({"error": "Missing required fields"}), 400
    
    new_id = db.next_equipment_id
    db.equipment_data[new_id] = {
        "id": new_id,
        "name": data.get('name'),
        "category": data.get('category'),
        "daily_rate": float(data.get('daily_rate', 0)),
        "quantity": int(data.get('quantity', 0)),
        "description": data.get('description', ''),
        "available": data.get('available', True)
    }
    db.next_equipment_id += 1
    return jsonify(db.equipment_data[new_id]), 201


@api_bp.route('/equipment/<int:id>', methods=['GET'])
def get_equipment_by_id(id):
    """
    Get equipment by ID
    ---
    tags:
      - Equipment
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      200:
        description: Equipment details
      404:
        description: Equipment not found
    """
    equipment = db.equipment_data.get(id)
    if not equipment:
        return jsonify({"error": "Equipment not found"}), 404
    return jsonify(equipment), 200


@api_bp.route('/equipment/<int:id>', methods=['PUT'])
def update_equipment(id):
    """
    Update equipment
    ---
    tags:
      - Equipment
    parameters:
      - in: path
        name: id
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
    equipment = db.equipment_data.get(id)
    if not equipment:
        return jsonify({"error": "Equipment not found"}), 404
    
    data = request.get_json()
    equipment.update({
        "name": data.get('name', equipment['name']),
        "category": data.get('category', equipment['category']),
        "daily_rate": float(data.get('daily_rate', equipment['daily_rate'])),
        "quantity": int(data.get('quantity', equipment['quantity'])),
        "description": data.get('description', equipment.get('description', '')),
        "available": data.get('available', equipment['available'])
    })
    return jsonify(equipment), 200


@api_bp.route('/equipment/<int:id>', methods=['DELETE'])
def delete_equipment(id):
    """
    Delete equipment
    ---
    tags:
      - Equipment
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      200:
        description: Equipment deleted successfully
      404:
        description: Equipment not found
    """
    if id not in db.equipment_data:
        return jsonify({"error": "Equipment not found"}), 404
    
    del db.equipment_data[id]
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
    return jsonify(list(db.customer_data.values())), 200


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
    if not data or not all(k in data for k in ['name', 'email', 'phone']):
        return jsonify({"error": "Missing required fields"}), 400
    
    email = data.get('email', '').strip().lower()
    
    # Validate email format
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return jsonify({"error": "Invalid email format"}), 400
    
    # Check for duplicate email
    if any(c['email'] == email for c in db.customer_data.values()):
        return jsonify({"error": "Email already exists"}), 400
    
    new_id = db.next_customer_id
    db.customer_data[new_id] = {
        "id": new_id,
        "name": data.get('name', '').strip(),
        "email": email,
        "phone": data.get('phone', '').strip(),
        "created_at": datetime.now().isoformat()
    }
    db.next_customer_id += 1
    return jsonify(db.customer_data[new_id]), 201


@api_bp.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    """
    Update customer
    ---
    tags:
      - Customers
    parameters:
      - in: path
        name: id
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
    customer = db.customer_data.get(id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    
    data = request.get_json()
    email = data.get('email', customer['email']).strip().lower()
    
    # Validate email format
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return jsonify({"error": "Invalid email format"}), 400
    
    # Check for duplicate email (excluding self)
    if any(c['email'] == email and c['id'] != id for c in db.customer_data.values()):
        return jsonify({"error": "Email already exists"}), 400
    
    customer.update({
        "name": data.get('name', customer['name']).strip(),
        "email": email,
        "phone": data.get('phone', customer['phone']).strip()
    })
    return jsonify(customer), 200


@api_bp.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    """
    Delete customer
    ---
    tags:
      - Customers
    parameters:
      - in: path
        name: id
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
    if id not in db.customer_data:
        return jsonify({"error": "Customer not found"}), 404
    
    # Check for active rentals
    active_rentals = [r for r in db.rental_data.values() 
                      if r['customer_id'] == id and r['status'] == 'active']
    if active_rentals:
        return jsonify({"error": "Cannot delete customer with active rentals"}), 400
    
    del db.customer_data[id]
    return jsonify({"message": "Customer deleted successfully"}), 200


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
    if not data or not all(k in data for k in ['equipment_id', 'customer_id', 'start_date', 'end_date']):
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
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
    
    new_id = db.next_rental_id
    db.rental_data[new_id] = {
        "id": new_id,
        "equipment_id": equipment_id,
        "customer_id": customer_id,
        "start_date": data['start_date'],
        "end_date": data['end_date'],
        "status": "active",
        "total_cost": total_cost
    }
    db.next_rental_id += 1
    return jsonify(db.rental_data[new_id]), 201


@api_bp.route('/rentals/<int:id>/return', methods=['PUT'])
def return_rental(id):
    """
    Mark rental as returned
    ---
    tags:
      - Rentals
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      200:
        description: Rental marked as returned
      404:
        description: Rental not found
    """
    rental = db.rental_data.get(id)
    if not rental:
        return jsonify({"error": "Rental not found"}), 404
    
    rental['status'] = 'returned'
    return jsonify(rental), 200
