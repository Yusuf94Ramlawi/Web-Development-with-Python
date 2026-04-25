"""
Equipment business logic service
Shared validation and CRUD operations for equipment
"""
import db


def validate_equipment_data(
    data,
    default_daily_rate=0,
    default_quantity=0,
    for_api=False
):
    """
    Validate equipment data from forms or API requests.

    Args:
        data: Form data dict or JSON dict
        default_daily_rate: Default value if parsing fails (for edits)
        default_quantity: Default value if parsing fails (for edits)
        for_api: True if validating API request (stricter validation)

    Returns:
        tuple: (errors dict, validated data dict)
    """
    errors = {}
    validated = {}

    # Name validation
    name = data.get('name', '').strip()
    if not name:
        errors['name'] = 'Name is required'
    validated['name'] = name

    # Category validation
    category = data.get('category', '').strip()
    if category == 'Other' and not for_api:
        category = data.get('other_category', '').strip()
    if not category:
        errors['category'] = 'Category is required'
    validated['category'] = category

    # Description validation
    description = data.get('description', '').strip()
    if not description:
        errors['description'] = 'Description is required'
    validated['description'] = description

    # Daily rate validation
    try:
        daily_rate = float(data.get('daily_rate', 0))
        if daily_rate <= 0:
            errors['daily_rate'] = 'Daily rate must be greater than 0'
    except (ValueError, TypeError):
        errors['daily_rate'] = 'Daily rate must be a valid number'
        daily_rate = default_daily_rate
    validated['daily_rate'] = daily_rate

    # Quantity validation
    try:
        quantity = int(data.get('quantity', 0))
        if quantity <= 0:
            errors['quantity'] = 'Quantity must be greater than 0'
    except (ValueError, TypeError):
        errors['quantity'] = 'Quantity must be a valid number'
        quantity = default_quantity
    validated['quantity'] = quantity

    # Available checkbox/boolean
    if for_api:
        validated['available'] = data.get('available', True)
    else:
        validated['available'] = (data.get('available') == '1')

    return errors, validated


def create_equipment(validated_data):
    """
    Create a new equipment record.

    Args:
        validated_data: Dictionary with validated equipment data

    Returns:
        dict: The created equipment record with ID
    """
    new_id = db.next_equipment_id
    db.equipment_data[new_id] = {
        "id": new_id,
        "name": validated_data['name'],
        "category": validated_data['category'],
        "daily_rate": validated_data['daily_rate'],
        "quantity": validated_data['quantity'],
        "description": validated_data['description'],
        "available": validated_data['available'],
    }
    db.next_equipment_id += 1
    return db.equipment_data[new_id]


def update_equipment(equipment_id, validated_data):
    """
    Update an existing equipment record.

    Args:
        equipment_id: ID of equipment to update
        validated_data: Dictionary with validated equipment data

    Returns:
        dict: The updated equipment record, or None if not found
    """
    equipment = db.equipment_data.get(equipment_id)
    if not equipment:
        return None

    equipment.update({
        "name": validated_data['name'],
        "category": validated_data['category'],
        "daily_rate": validated_data['daily_rate'],
        "quantity": validated_data['quantity'],
        "description": validated_data['description'],
        "available": validated_data['available'],
    })
    return equipment


def get_equipment_by_id(equipment_id):
    """
    Get equipment by ID.

    Args:
        equipment_id: ID of equipment to retrieve

    Returns:
        dict: Equipment record or None if not found
    """
    return db.equipment_data.get(equipment_id)


def get_all_equipment():
    """
    Get all equipment records.

    Returns:
        list: List of all equipment records
    """
    return list(db.equipment_data.values())


def delete_equipment(equipment_id):
    """
    Delete an equipment record.

    Args:
        equipment_id: ID of equipment to delete

    Returns:
        bool: True if deleted, False if not found
    """
    if equipment_id in db.equipment_data:
        del db.equipment_data[equipment_id]
        return True
    return False


def get_categories():
    """
    Get all unique equipment categories.

    Returns:
        set: Set of category strings
    """
    return set(e['category'] for e in db.equipment_data.values())
