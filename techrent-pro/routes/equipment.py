
import db
from flask import (
    Blueprint, redirect, render_template, request, url_for, flash
)
from utils.pagination import Paginator
from services import equipment_service

equipment_bp = Blueprint("equipment", __name__, url_prefix="/equipment")


@equipment_bp.route('/', methods=['GET'])
def get_equipment():
    selected_category = request.args.get('category', '').strip()
    search_query = request.args.get('q', '').strip()

    equipments = equipment_service.get_all_equipment()
    categories = equipment_service.get_categories()

    if selected_category:
        equipments = [eq for eq in equipments if eq['category']
                      == selected_category]
    if search_query:
        equipments = [eq for eq in equipments if search_query.lower()
                      in eq['name'].lower()]
    pager = Paginator()
    result = pager.paginate(equipments)
    return render_template('equipment/list.html', equipment_list=result['data'], categories=categories, selected_category=selected_category, search_query=search_query, pagination=result['pagination'])


@equipment_bp.route('/add', methods=['GET', 'POST'])
def add_equipment():
    if request.method == 'POST':
        form_data = request.form

        # Server-side validation using service layer
        errors, validated = equipment_service.validate_equipment_data(
            form_data
        )

        if errors:
            categories = equipment_service.get_categories()
            return render_template(
                'equipment/form.html',
                form_data=form_data,
                categories=categories,
                mode='add',
                errors=errors
            )

        equipment_service.create_equipment(validated)
        flash('Equipment added successfully!', 'success')
        return redirect(url_for('equipment.get_equipment'))

    categories = equipment_service.get_categories()
    return render_template(
        'equipment/form.html',
        form_data={},
        categories=categories,
        mode='add'
    )


@equipment_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_equipment(id):
    equipment = equipment_service.get_equipment_by_id(id)
    if not equipment:
        return render_template('404.html', message="Equipment not found."), 404

    if request.method == 'POST':
        form_data = request.form

        # Server-side validation using service layer
        # Pass current values as defaults for failed parsing
        errors, validated = equipment_service.validate_equipment_data(
            form_data,
            default_daily_rate=equipment['daily_rate'],
            default_quantity=equipment['quantity']
        )

        if errors:
            categories = equipment_service.get_categories()
            return render_template(
                'equipment/form.html',
                id=id,
                form_data=form_data,
                categories=categories,
                mode='edit',
                errors=errors
            )

        equipment_service.update_equipment(id, validated)
        flash('Equipment updated successfully!', 'success')
        return redirect(url_for('equipment.view_equipment', id=id))

    categories = equipment_service.get_categories()
    return render_template(
        'equipment/form.html',
        id=id,
        form_data=equipment,
        categories=categories,
        mode='edit'
    )


@equipment_bp.route('/delete/<int:id>', methods=['POST'])
def delete_equipment(id):
    equipment_service.delete_equipment(id)
    return redirect(url_for('equipment.get_equipment'))


@equipment_bp.route('/<int:id>')
def view_equipment(id):
    equipment = equipment_service.get_equipment_by_id(id)
    if not equipment:
        return render_template('404.html', message="Equipment not found."), 404
    customers = db.customer_data
    rentals = [r for r in db.rental_data.values() if r['equipment_id'] == id]
    available_quantity = equipment['quantity'] - \
        sum(1 for r in rentals if r['status'] == 'active')
    equipment_rentals = []
    for rental in rentals:
        customer = customers.get(rental['customer_id'])
        equipment_rentals.append({
            'customer': customer['name'] if customer else 'Unknown',
            'start_date': rental['start_date'],
            'end_date': rental['end_date'],
            'status': rental['status'],
            'cost': rental['total_cost']
        })
    return render_template('equipment/detail.html', equipment=equipment, rentals=equipment_rentals, available_quantity=available_quantity)
