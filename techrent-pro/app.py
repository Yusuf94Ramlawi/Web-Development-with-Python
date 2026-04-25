import os

from flask import Flask, render_template, request, jsonify
from flasgger import Swagger
from routes.rentals import rentals_bp
from routes.dashboard import dashboard
from routes.equipment import equipment_bp
from routes.customers import customers_bp
from routes.api import api_bp
from routes.doc import swagger_bp
from routes.reports import reports_bp


app = Flask(__name__)
app.secret_key = (
    'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
)

app.register_blueprint(dashboard)
app.register_blueprint(rentals_bp)
app.register_blueprint(equipment_bp)
app.register_blueprint(customers_bp)
app.register_blueprint(api_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(swagger_bp)

swagger = Swagger(app)


@app.errorhandler(404)
def not_found_error(error):
    # Return JSON for API requests, HTML for regular requests
    if request.path.startswith('/api/'):
        return jsonify({"error": "Resource not found"}), 404
    return render_template('404.html', message="Page not found"), 404


@app.errorhandler(500)
def internal_error(error):
    # Return JSON for API requests, HTML for regular requests
    if request.path.startswith('/api/'):
        return jsonify({"error": "Internal server error"}), 500
    return render_template('500.html', message="Internal server error"), 500


if __name__ == '__main__':
    is_debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=True, host='0.0.0.0', port=5000)
