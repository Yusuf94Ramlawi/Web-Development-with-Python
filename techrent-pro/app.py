import os

from flask import Flask
from flasgger import Swagger
from routes.rentals import rentals_bp
from routes.dashboard import dashboard
from routes.equipment import equipment_bp
from routes.customers import customers_bp
from routes.api import api_bp
from routes.doc import swagger_bp
from routes.reports import reports_bp
from routes.errorhandler import err_handler_bp


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
app.register_blueprint(err_handler_bp)
app.register_blueprint(swagger_bp)

swagger = Swagger(app)


if __name__ == '__main__':
    is_debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=is_debug, host='0.0.0.0', port=5000)
