import db
from flask import Blueprint, redirect, render_template, request, url_for, flash
import re
from datetime import datetime

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")


@customers_bp.route('/')
def customers():
    q = request.args.get('q', '').strip().lower()
    customers = list(db.customer_data.values())
    if q:
        customers = [c for c in customers if q in c['name'].lower()
                     or q in c['email'].lower()]
    customers = sorted(customers, key=lambda c: c['name'].lower())
    return render_template('customers/list.html', customers=customers, search_query=q)


@customers_bp.route('/add', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        form_data = request.form

        is_unique_email = not any(c['email'] == form_data.get(
            'email', '').strip().lower() for c in db.customer_data.values())
        if (is_unique_email == False):
            flash('Email already exists.', 'danger')
            return render_template('customers/form.html', form_data=form_data)

        db.customer_data[db.next_customer_id] = {
            'id': db.next_customer_id,
            'name': form_data.get('name', '').strip(),
            'email': form_data.get('email', '').strip().lower(),
            'phone': form_data.get('phone', '').strip(),
            'created_at': datetime.now().isoformat()
        }
        db.next_customer_id += 1
        flash('Customer registered successfully!', 'success')
        return redirect(url_for('customers.customers'))
    return render_template('customers/form.html', form_data={})


@customers_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    customer = db.customer_data.get(id)
    if not customer:
        return render_template('404.html', message="Customer not found."), 404
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        # Email uniqueness (ignore self)
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            error = 'Invalid email format.'
        elif any(c['email'] == email and c['id'] != id for c in db.customer_data.values()):
            error = 'Email already exists.'
        else:
            error = None
        if error:
            flash(error, 'danger')
            return render_template('customers/form.html', form_data={'name': name, 'email': email, 'phone': phone}, id=id)
        customer['name'] = name
        customer['email'] = email
        customer['phone'] = phone
        flash('Customer updated successfully!', 'success')
        return redirect(url_for('customers.customers'))
    return render_template('customers/form.html', form_data=customer, id=id)


@customers_bp.route('/delete/<int:id>', methods=['POST'])
def delete_customer(id):
    active_rentals = [r for r in db.rental_data.values(
    ) if r['customer_id'] == id and r['status'] == 'active']
    if active_rentals:
        flash('Cannot delete customer with active rentals.', 'danger')
        return redirect(url_for('customers.customers'))
    db.customer_data.pop(id, None)
    flash('Customer deleted successfully.', 'success')
    return redirect(url_for('customers.customers'))
