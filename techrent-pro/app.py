from flask import Flask, render_template, request, redirect, url_for
from routes.rentals import rentals_bp
from routes.dashboard import dashboard
from routes.equipment import equipment_bp
from routes.customers import customers_bp
app = Flask(__name__)
app.secret_key = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'

app.register_blueprint(dashboard)
app.register_blueprint(rentals_bp)
app.register_blueprint(equipment_bp)
app.register_blueprint(customers_bp)

@app.route('/reports')
def reports():
    return render_template('reports/index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)