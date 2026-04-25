
import db
from flask import Blueprint, redirect, render_template, request, url_for
from utils.pagination import Paginator

equipment_bp = Blueprint("equipment", __name__, url_prefix="/equipment")


@equipment_bp.route('/', methods=['GET'])
def get_equipment():
    selected_category = request.args.get('category', '').strip()
    search_query = request.args.get('q', '').strip()

    equipments = list(db.equipment_data.values())
    categories = set(e['category'] for e in equipments)

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
        from_data = request.form
        db.equipment_data[db.next_equipment_id] = {
            "id": db.next_equipment_id,
            "name": from_data.get('name'),
            "category": from_data.get('category') if from_data.get('category') != "Other" else from_data.get("other_category"),
            "daily_rate": float(from_data.get('daily_rate', 0)),
            "quantity": int(from_data.get('quantity', 0)),
            "description": from_data.get('description'),
            "available": (from_data.get('available') == '1')
        }
        db.next_equipment_id += 1
        return redirect(url_for('equipment.get_equipment'))

    categories = set(e['category'] for e in db.equipment_data.values())
    return render_template('equipment/form.html', form_data={}, categories=categories, mode='add')


@equipment_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_equipment(id):
    equipment = db.equipment_data.get(id)
    if not equipment:
        return render_template('404.html', message="Equipment not found."), 404

    if request.method == 'POST':
        from_data = request.form
        if (from_data.get("other_category") and from_data.get("category") == "Other"):
            equipment['category'] = from_data.get("other_category")
        else:
            equipment['category'] = from_data.get('category')
        equipment['name'] = from_data.get('name')
        equipment['daily_rate'] = float(from_data.get('daily_rate', 0))
        equipment['quantity'] = int(from_data.get('quantity', 0))
        equipment['description'] = from_data.get('description')
        equipment['available'] = (from_data.get('available') == '1')

        return redirect(url_for('equipment.get_equipment'))
    categories = set(e['category'] for e in db.equipment_data.values())
    return render_template('equipment/form.html', id=id, form_data=equipment, categories=categories, mode='edit')


@equipment_bp.route('/delete/<int:id>', methods=['POST'])
def delete_equipment(id):
    if id in db.equipment_data:
        del db.equipment_data[id]
    return redirect(url_for('equipment.get_equipment'))


@equipment_bp.route('/<int:id>')
def view_equipment(id):
    equipment = db.equipment_data.get(id)
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
