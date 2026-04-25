import db
from flask import Blueprint, redirect, render_template, request, url_for, flash
from utils.pagination import Paginator
from services import customer_service

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")


@customers_bp.route('/')
def customers():
    q = request.args.get('q', '').strip().lower()
    customers = customer_service.get_all_customers()
    if q:
        customers = [c for c in customers if q in c['name'].lower()
                     or q in c['email'].lower()]
    customers = sorted(customers, key=lambda c: c['name'].lower())
    pager = Paginator()
    result = pager.paginate(customers)
    return render_template('customers/list.html', customers=result['data'], search_query=q, pagination=result['pagination'])


@customers_bp.route('/add', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        form_data = request.form
        name = form_data.get('name', '').strip()
        email = form_data.get('email', '').strip()
        phone = form_data.get('phone', '').strip()

        # Server-side validation using service layer
        errors = customer_service.validate_customer_data(
            {'name': name, 'email': email, 'phone': phone}
        )

        if errors:
            # Flash first error message
            first_error = next(iter(errors.values()))
            flash(first_error, 'danger')
            return render_template('customers/form.html', form_data=form_data)

        customer_service.create_customer(name, email, phone)
        flash('Customer registered successfully!', 'success')
        return redirect(url_for('customers.customers'))
    return render_template('customers/form.html', form_data={})


@customers_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    customer = customer_service.get_customer_by_id(id)
    if not customer:
        return render_template('404.html', message="Customer not found."), 404

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()

        # Server-side validation using service layer
        errors = customer_service.validate_customer_data(
            {'name': name, 'email': email, 'phone': phone},
            customer_id=id
        )

        if errors:
            # Flash first error message
            first_error = next(iter(errors.values()))
            flash(first_error, 'danger')
            form_data = {'name': name, 'email': email, 'phone': phone}
            return render_template('customers/form.html', form_data=form_data, id=id)

        customer_service.update_customer(id, name, email, phone)
        flash('Customer updated successfully!', 'success')
        return redirect(url_for('customers.customers'))

    return render_template('customers/form.html', form_data=customer, id=id)


@customers_bp.route('/delete/<int:id>', methods=['POST'])
def delete_customer(id):
    success, message = customer_service.delete_customer(id)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')
    return redirect(url_for('customers.customers'))
