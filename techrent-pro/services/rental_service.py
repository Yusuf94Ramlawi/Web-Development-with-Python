"""
Rental business logic service
Shared validation and operations for rentals
"""
import db
import datetime


def calculate_total_cost(equipment_id, start_date, end_date):
    """
    Calculate total rental cost based on equipment daily rate and date range.

    Args:
        equipment_id: ID of equipment to rent
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)

    Returns:
        float: Total cost, or 0.0 if equipment not found
    """
    equipment = db.equipment_data.get(int(equipment_id))
    if not equipment:
        return 0.0

    daily_rate = equipment.get("daily_rate", 0.0)
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    days = (end - start).days + 1
    return round(daily_rate * days, 2)


def check_overlap_booking(
    equipment_id, start_date, end_date, exclude_rental_id=None
):
    """
    Check if equipment is already booked for the specified date range.

    Args:
        equipment_id: ID of equipment to check
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)
        exclude_rental_id: Optional rental ID to exclude from check (for edits)

    Returns:
        bool: True if there's an overlapping booking
    """
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    for rental in db.rental_data.values():
        if exclude_rental_id is not None and rental["id"] == exclude_rental_id:
            continue

        if (
            rental["equipment_id"] == int(equipment_id)
            and str(rental.get("status", "")).lower() == "active"
        ):
            existing_start = datetime.datetime.strptime(
                rental["start_date"], "%Y-%m-%d"
            )
            existing_end = datetime.datetime.strptime(
                rental["end_date"], "%Y-%m-%d"
            )

            if start <= existing_end and end >= existing_start:
                return True

    return False


def validate_rental_data(data, for_api=False):
    """
    Validate rental data from forms or API requests.

    Args:
        data: Form data dict or JSON dict
        for_api: True if validating API request

    Returns:
        tuple: (errors dict, validated data dict)
    """
    errors = {}
    validated = {}

    # Equipment ID validation
    try:
        equipment_id = int(data.get('equipment_id', 0))
        if equipment_id not in db.equipment_data:
            errors['equipment_id'] = 'Equipment not found'
        validated['equipment_id'] = equipment_id
    except (ValueError, TypeError):
        errors['equipment_id'] = 'Invalid equipment ID'
        validated['equipment_id'] = 0

    # Customer ID validation
    try:
        customer_id = int(data.get('customer_id', 0))
        if customer_id not in db.customer_data:
            errors['customer_id'] = 'Customer not found'
        validated['customer_id'] = customer_id
    except (ValueError, TypeError):
        errors['customer_id'] = 'Invalid customer ID'
        validated['customer_id'] = 0

    # Date validation
    start_date = data.get('start_date', '').strip()
    end_date = data.get('end_date', '').strip()

    if not start_date:
        errors['start_date'] = 'Start date is required'
    if not end_date:
        errors['end_date'] = 'End date is required'

    if start_date and end_date:
        try:
            start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            days = (end - start).days + 1
            if days <= 0:
                errors['date_range'] = 'End date must be after start date'
        except ValueError:
            errors['date_format'] = 'Invalid date format. Use YYYY-MM-DD'

    validated['start_date'] = start_date
    validated['end_date'] = end_date

    # Status validation
    status = data.get('status', 'active').strip().lower()
    allowed_statuses = {'active', 'returned', 'overdue'}
    if status not in allowed_statuses:
        errors['status'] = (
            'Invalid status. Allowed values: active, returned, overdue'
        )
        status = 'active'
    validated['status'] = status

    return errors, validated


def create_rental(equipment_id, customer_id, start_date, end_date):
    """
    Create a new rental record.

    Args:
        equipment_id: ID of equipment to rent
        customer_id: ID of customer renting
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)

    Returns:
        dict: The created rental record with ID
    """
    total_cost = calculate_total_cost(equipment_id, start_date, end_date)
    new_id = db.next_rental_id
    db.rental_data[new_id] = {
        "id": new_id,
        "equipment_id": int(equipment_id),
        "customer_id": int(customer_id),
        "start_date": start_date,
        "end_date": end_date,
        "status": "active",
        "total_cost": total_cost,
    }
    db.next_rental_id += 1
    return db.rental_data[new_id]


def update_rental(rental_id, equipment_id, customer_id, start_date, end_date, status):
    """
    Update an existing rental record.

    Args:
        rental_id: ID of rental to update
        equipment_id: ID of equipment
        customer_id: ID of customer
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)
        status: Rental status (active/returned/overdue)

    Returns:
        dict: The updated rental record, or None if not found
    """
    rental = db.rental_data.get(rental_id)
    if not rental:
        return None

    rental["equipment_id"] = int(equipment_id)
    rental["customer_id"] = int(customer_id)
    rental["start_date"] = start_date
    rental["end_date"] = end_date
    rental["status"] = status
    rental["total_cost"] = calculate_total_cost(
        equipment_id, start_date, end_date
    )
    return rental


def update_rental_status(rental_id, status):
    """
    Update only the status of a rental.

    Args:
        rental_id: ID of rental to update
        status: New status (active/returned/overdue)

    Returns:
        dict: The updated rental record, or None if not found
    """
    rental = db.rental_data.get(rental_id)
    if not rental:
        return None

    rental['status'] = status
    return rental


def get_rental_by_id(rental_id):
    """
    Get rental by ID.

    Args:
        rental_id: ID of rental to retrieve

    Returns:
        dict: Rental record or None if not found
    """
    return db.rental_data.get(rental_id)


def get_all_rentals():
    """
    Get all rental records.

    Returns:
        list: List of all rental records
    """
    return list(db.rental_data.values())


def build_rental_view(rental):
    """
    Build a rental view with denormalized customer and equipment data.

    Args:
        rental: Rental record dict

    Returns:
        dict: Enriched rental view with customer and equipment names
    """
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


def get_available_equipment():
    """
    Get all equipment that is available for rental.
    Considers both the available flag and quantity vs active rentals.

    Returns:
        list: List of available equipment records
    """
    equipment = []
    for eq in db.equipment_data.values():
        if eq["available"]:
            active_rentals = sum(
                1 for r in db.rental_data.values()
                if r["equipment_id"] == eq["id"] and r["status"] == "active"
            )
            if eq["quantity"] > active_rentals:
                equipment.append(eq)
    return equipment
