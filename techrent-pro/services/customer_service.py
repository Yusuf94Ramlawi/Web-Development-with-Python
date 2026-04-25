"""
Customer business logic service
Shared validation and CRUD operations for customers
"""
import db
import re
from datetime import datetime


def validate_customer_data(data, customer_id=None, for_api=False):
    """
    Validate customer data from forms or API requests.

    Args:
        data: Form data dict or JSON dict
        customer_id: Optional ID to exclude from uniqueness check (for edits)
        for_api: True if validating API request

    Returns:
        dict: Error messages keyed by field name, or empty dict if valid
    """
    errors = {}

    # Name validation
    name = data.get('name', '').strip()
    if not name:
        errors['name'] = 'Name is required.'

    # Email validation
    email = data.get('email', '').strip()
    if not for_api:
        email = email.lower()

    if not email:
        errors['email'] = 'Email is required.'
    elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        errors['email'] = 'Invalid email format.'
    else:
        # Check email uniqueness
        email_to_check = email.lower()
        is_duplicate = any(
            c['email'] == email_to_check and c['id'] != customer_id
            for c in db.customer_data.values()
        )
        if is_duplicate:
            errors['email'] = 'Email already exists.'

    # Phone validation
    phone = data.get('phone', '').strip()
    if not phone:
        errors['phone'] = 'Phone is required.'

    return errors


def create_customer(name, email, phone):
    """
    Create a new customer record.

    Args:
        name: Customer name
        email: Customer email (will be lowercased)
        phone: Customer phone

    Returns:
        dict: The created customer record with ID
    """
    new_id = db.next_customer_id
    db.customer_data[new_id] = {
        'id': new_id,
        'name': name.strip(),
        'email': email.strip().lower(),
        'phone': phone.strip(),
        'created_at': datetime.now().isoformat(),
    }
    db.next_customer_id += 1
    return db.customer_data[new_id]


def update_customer(customer_id, name, email, phone):
    """
    Update an existing customer record.

    Args:
        customer_id: ID of customer to update
        name: Customer name
        email: Customer email (will be lowercased)
        phone: Customer phone

    Returns:
        dict: The updated customer record, or None if not found
    """
    customer = db.customer_data.get(customer_id)
    if not customer:
        return None

    customer['name'] = name.strip()
    customer['email'] = email.strip().lower()
    customer['phone'] = phone.strip()
    return customer


def get_customer_by_id(customer_id):
    """
    Get customer by ID.

    Args:
        customer_id: ID of customer to retrieve

    Returns:
        dict: Customer record or None if not found
    """
    return db.customer_data.get(customer_id)


def get_all_customers():
    """
    Get all customer records.

    Returns:
        list: List of all customer records
    """
    return list(db.customer_data.values())


def delete_customer(customer_id):
    """
    Delete a customer record.

    Args:
        customer_id: ID of customer to delete

    Returns:
        tuple: (success: bool, message: str)
    """
    if customer_id not in db.customer_data:
        return False, "Customer not found"

    # Check for active rentals
    active_rentals = [
        r for r in db.rental_data.values()
        if r['customer_id'] == customer_id and r['status'] == 'active'
    ]

    if active_rentals:
        return False, "Cannot delete customer with active rentals"

    del db.customer_data[customer_id]
    return True, "Customer deleted successfully"


def has_active_rentals(customer_id):
    """
    Check if customer has any active rentals.

    Args:
        customer_id: ID of customer to check

    Returns:
        bool: True if customer has active rentals
    """
    return any(
        r['customer_id'] == customer_id and r['status'] == 'active'
        for r in db.rental_data.values()
    )
