from flask import (
    Blueprint, redirect, render_template, request, url_for, flash
)
from utils.pagination import Paginator
from services import frontend_api_service

equipment_bp = Blueprint("equipment", __name__, url_prefix="/equipment")


def _build_equipment_payload(form_data):
    """Build JSON payload expected by equipment API endpoints."""
    category = form_data.get('category', '').strip()
    if category == 'Other':
        category = form_data.get('other_category', '').strip()

    return {
        'name': form_data.get('name', '').strip(),
        'category': category,
        'daily_rate': form_data.get('daily_rate', '').strip(),
        'quantity': form_data.get('quantity', '').strip(),
        'description': form_data.get('description', '').strip(),
        'available': form_data.get('available') == '1',
    }


@equipment_bp.route('/', methods=['GET'])
def get_equipment():
    """
    List equipment with optional category/search filtering and pagination.

    Args:
        None

    Returns:
        Response: Rendered equipment list page.
    """
    selected_category = request.args.get('category', '').strip()
    search_query = request.args.get('q', '').strip()

    status_code, payload = frontend_api_service.get('/api/equipment')
    equipments = payload if status_code == 200 and isinstance(
        payload, list) else []
    categories = sorted({item.get('category', '')
                        for item in equipments if item.get('category')})

    if status_code != 200:
        flash('Unable to load equipment from API.', 'danger')

    if selected_category:
        equipments = [eq for eq in equipments if eq['category']
                      == selected_category]
    if search_query:
        equipments = [eq for eq in equipments if search_query.lower()
                      in eq['name'].lower()]
    pager = Paginator()
    result = pager.paginate(equipments)
    return render_template('equipment/list.html', equipment_list=result['data'], categories=categories, selected_category=selected_category, search_query=search_query, pagination=result['pagination'])


@equipment_bp.route('/<int:id>', methods=['GET'])
def view_equipment(id):
    """
    Show one equipment record and related rental history.

    Args:
        id: Equipment identifier.

    Returns:
        Response: Rendered equipment details page.
    """
    equipment_status, equipment = frontend_api_service.get(
        f'/api/equipment/{id}')
    if equipment_status != 200:
        message = equipment.get('error', 'Equipment not found.')
        return render_template('404.html', message=message), 404

    rentals_status, rentals_payload = frontend_api_service.get('/api/rentals')
    rentals_data = (
        rentals_payload
        if rentals_status == 200 and isinstance(rentals_payload, list)
        else []
    )

    rentals = [r for r in rentals_data if r.get('equipment_id') == id]
    available_quantity = equipment['quantity'] - sum(
        1 for r in rentals if str(r.get('status', '')).lower() == 'active'
    )

    equipment_rentals = []
    for rental in rentals:
        equipment_rentals.append({
            'customer': rental.get('customer_name', 'Unknown'),
            'start_date': rental['start_date'],
            'end_date': rental['end_date'],
            'status': rental['status'],
            'cost': rental['total_cost']
        })
    return render_template('equipment/detail.html', equipment=equipment, rentals=equipment_rentals, available_quantity=available_quantity)


@equipment_bp.route('/new', methods=['GET', 'POST'])
def add_equipment():
    """
    Create a new equipment record from form input.

    Args:
        None

    Returns:
        Response: Equipment form or redirect to equipment list on success.
    """
    if request.method == 'POST':
        form_data = request.form.to_dict(flat=True)
        payload = _build_equipment_payload(form_data)

        status_code, response_data = frontend_api_service.post(
            '/api/equipment',
            json_data=payload,
        )

        if status_code != 201:
            errors = frontend_api_service.extract_errors(response_data)
            equipment_status, equipment_payload = frontend_api_service.get(
                '/api/equipment')
            categories = sorted({
                item.get('category', '')
                for item in (equipment_payload if equipment_status == 200 and isinstance(equipment_payload, list) else [])
                if item.get('category')
            })
            return render_template(
                'equipment/form.html',
                form_data=form_data,
                categories=categories,
                mode='add',
                errors=errors
            )

        flash('Equipment added successfully!', 'success')
        return redirect(url_for('equipment.get_equipment'))

    equipment_status, equipment_payload = frontend_api_service.get(
        '/api/equipment')
    categories = sorted({
        item.get('category', '')
        for item in (equipment_payload if equipment_status == 200 and isinstance(equipment_payload, list) else [])
        if item.get('category')
    })
    return render_template(
        'equipment/form.html',
        form_data={},
        categories=categories,
        mode='add',
        errors={}
    )


@equipment_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_equipment(id):
    """
    Edit an existing equipment record.

    Args:
        id: Equipment identifier.

    Returns:
        Response: Equipment form or redirect to equipment details on success.
    """
    equipment_status, equipment = frontend_api_service.get(
        f'/api/equipment/{id}')
    if equipment_status != 200:
        message = equipment.get('error', 'Equipment not found.')
        return render_template('404.html', message=message), 404

    if request.method == 'POST':
        form_data = request.form.to_dict(flat=True)
        payload = _build_equipment_payload(form_data)

        update_status, response_data = frontend_api_service.put(
            f'/api/equipment/{id}',
            json_data=payload,
        )

        if update_status != 200:
            errors = frontend_api_service.extract_errors(response_data)
            equipment_list_status, equipment_payload = frontend_api_service.get(
                '/api/equipment')
            categories = sorted({
                item.get('category', '')
                for item in (equipment_payload if equipment_list_status == 200 and isinstance(equipment_payload, list) else [])
                if item.get('category')
            })
            return render_template(
                'equipment/form.html',
                id=id,
                form_data=form_data,
                categories=categories,
                mode='edit',
                errors=errors
            )

        flash('Equipment updated successfully!', 'success')
        return redirect(url_for('equipment.view_equipment', id=id))

    equipment_list_status, equipment_payload = frontend_api_service.get(
        '/api/equipment')
    categories = sorted({
        item.get('category', '')
        for item in (equipment_payload if equipment_list_status == 200 and isinstance(equipment_payload, list) else [])
        if item.get('category')
    })
    return render_template(
        'equipment/form.html',
        id=id,
        form_data=equipment,
        categories=categories,
        mode='edit',
        errors={}
    )


@equipment_bp.route('/<int:id>/delete', methods=['DELETE'])
def delete_equipment(id):
    """
    Delete an equipment record.

    Args:
        id: Equipment identifier.

    Returns:
        Response: Redirect to equipment list.
    """
    status_code, payload = frontend_api_service.delete(f'/api/equipment/{id}')
    if status_code == 200:
        flash(payload.get('message', 'Equipment deleted successfully'), 'success')
    else:
        flash(payload.get('error', 'Unable to delete equipment'), 'danger')
    return redirect(url_for('equipment.get_equipment'))
