from flask import Flask, render_template, request, redirect, url_for
from routes.rentals import rentals_bp
from routes.dashboard import dashboard

app = Flask(__name__)

app.register_blueprint(dashboard)
app.register_blueprint(rentals_bp)


@app.route('/equipment')
def equipment():
    return render_template('equipment/list.html')

@app.route('/equipment/add', methods=['GET', 'POST'])
def add_equipment():
    if request.method == 'POST':
        return redirect(url_for('equipment'))
    return render_template('equipment/form.html')

@app.route('/equipment/edit/<int:id>', methods=['GET', 'POST'])
def edit_equipment(id):
    if request.method == 'POST':
        return redirect(url_for('equipment'))
    return render_template('equipment/form.html', id=id)

@app.route('/equipment/delete/<int:id>', methods=['POST'])
def delete_equipment(id):
    return redirect(url_for('equipment'))

@app.route('/equipment/<int:id>')
def view_equipment(id):
    return render_template('equipment/detail.html', id=id)


@app.route('/customers')
def customers():
    return render_template('customers/list.html')

@app.route('/customers/add', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        return redirect(url_for('customers'))
    return render_template('customers/form.html')

@app.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    if request.method == 'POST':
        return redirect(url_for('customers'))
    return render_template('customers/form.html', id=id)

@app.route('/customers/delete/<int:id>', methods=['POST'])
def delete_customer(id):
    return redirect(url_for('customers'))

@app.route('/reports')
def reports():
    return render_template('reports/index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)