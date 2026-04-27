from flask import Blueprint, redirect, render_template, request, url_for, flash
from utils.pagination import Paginator
from services import frontend_api_service

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")


@customers_bp.route('/')
def customers():
    """
    List customers with optional search and pagination.

    Args:
        None

    Returns:
        Response: Rendered customers list page.
    """
    q = request.args.get('q', '').strip().lower()
    status_code, payload = frontend_api_service.get('/api/customers')
    customers = payload if status_code == 200 and isinstance(
        payload, list) else []

    if status_code != 200:
        flash('Unable to load customers from API.', 'danger')

    if q:
        customers = [c for c in customers if q in c['name'].lower()
                     or q in c['email'].lower()]
    customers = sorted(customers, key=lambda c: c['name'].lower())
    pager = Paginator()
    result = pager.paginate(customers)
    return render_template('customers/list.html', customers=result['data'], search_query=q, pagination=result['pagination'])


@customers_bp.route('/add', methods=['GET', 'POST'])
def add_customer():
    """
    Create a customer from form input.

    Args:
        None

    Returns:
        Response: Customer form or redirect to customer list on success.
    """
    if request.method == 'POST':
        form_data = {
            'name': request.form.get('name', '').strip(),
            'email': request.form.get('email', '').strip(),
            'phone': request.form.get('phone', '').strip(),
        }

        status_code, payload = frontend_api_service.post(
            '/api/customers',
            json_data=form_data,
        )

        if status_code != 201:
            errors = frontend_api_service.extract_errors(payload)
            return render_template(
                'customers/form.html',
                form_data=form_data,
                errors=errors
            ), 400

        flash('Customer registered successfully!', 'success')
        return redirect(url_for('customers.customers'))
    return render_template('customers/form.html', form_data={}, errors={})


@customers_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    """
    Edit an existing customer.

    Args:
        id: Customer identifier.

    Returns:
        Response: Customer form or redirect to customer list on success.
    """
    status_code, customer = frontend_api_service.get(f'/api/customers/{id}')
    if status_code != 200:
        message = customer.get('error', 'Customer not found.')
        return render_template('404.html', message=message), 404

    if request.method == 'POST':
        form_data = {
            'name': request.form.get('name', '').strip(),
            'email': request.form.get('email', '').strip(),
            'phone': request.form.get('phone', '').strip(),
        }

        update_status, payload = frontend_api_service.put(
            f'/api/customers/{id}',
            json_data=form_data,
        )

        if update_status != 200:
            errors = frontend_api_service.extract_errors(payload)
            return render_template(
                'customers/form.html',
                form_data=form_data,
                id=id,
                errors=errors
            ), 400

        flash('Customer updated successfully!', 'success')
        return redirect(url_for('customers.customers'))

    return render_template(
        'customers/form.html',
        form_data=customer,
        id=id,
        errors={}
    )


@customers_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_customer(id):
    """
    Delete a customer.

    Args:
        id: Customer identifier.

    Returns:
        Response: Redirect to customer list with flash message.
    """
    status_code, payload = frontend_api_service.delete(f'/api/customers/{id}')
    if status_code == 200:
        flash(payload.get('message', 'Customer deleted successfully'), 'success')
    else:
        flash(payload.get('error', 'Unable to delete customer'), 'danger')
    return redirect(url_for('customers.customers'))
