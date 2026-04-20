
import db
from flask import Blueprint, redirect, render_template, request, url_for

equipment_bp = Blueprint("equipment", __name__, url_prefix="/equipment")

@equipment_bp.route('/')
def equipment():
    equipments = db.equipment_data
    categories = set(e['category'] for e in equipments.values())
    categories.add('All')
    return render_template('equipment/list.html', equipment_list=equipments, categories=categories)

@equipment_bp.route('/add', methods=['GET', 'POST'])
def add_equipment():
    if request.method == 'POST':
        return redirect(url_for('equipment.equipment'))
    return render_template('equipment/form.html')

@equipment_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_equipment(id):
    if request.method == 'POST':
        return redirect(url_for('equipment.equipment'))
    return render_template('equipment/form.html', id=id)

@equipment_bp.route('/delete/<int:id>', methods=['POST'])
def delete_equipment(id):
    return redirect(url_for('equipment.equipment'))

@equipment_bp.route('/<int:id>')
def view_equipment(id):
    equipment = db.equipment_data.get(id)
    customers = db.customer_data
    rentals = [r for r in db.rental_data.values() if r['equipment_id'] == id]
    available_quantity = equipment['quantity'] - sum(1 for r in rentals if r['status'] == 'active')
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
