
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
    return render_template('equipment/detail.html', id=id)
