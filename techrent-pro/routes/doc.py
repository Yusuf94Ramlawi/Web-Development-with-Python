from flask import Blueprint, render_template

swagger_bp = Blueprint("swagger", __name__)


@swagger_bp.route('/api-docs/')
def api_docs():
    return render_template('swaggerui.html')
