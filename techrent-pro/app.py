from flask import Flask, render_template, request, redirect, url_for
from routes.rentals import rentals_bp
from routes.dashboard import dashboard
from routes.equipment import equipment_bp

app = Flask(__name__)

app.register_blueprint(dashboard)
app.register_blueprint(rentals_bp)
app.register_blueprint(equipment_bp)




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