import db
from flask import Blueprint, redirect, render_template, request, url_for

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

@customers_bp.route('/')
def customers():
    customers = db.customer_data.values()
    return render_template('customers/list.html', customers=customers)

@customers_bp.route('/add', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        return redirect(url_for('customers.customers'))
    return render_template('customers/form.html')

@customers_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_customer(id):
    if request.method == 'POST':
        return redirect(url_for('customers.customers'))
    return render_template('customers/form.html', id=id)

@customers_bp.route('/<int:id>/delete', methods=['POST'])
def delete_customer(id):
    return redirect(url_for('customers.customers'))