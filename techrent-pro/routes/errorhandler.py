
from flask import (
    Blueprint, jsonify, render_template, request
)
from utils.pagination import Paginator
from services import equipment_service

err_handler_bp = Blueprint("errorhandler", __name__,)


@err_handler_bp.errorhandler(404)
def not_found_error(error):
    # Return JSON for API requests, HTML for regular requests
    if request.path.startswith('/api/'):
        return jsonify({"error": "Resource not found"}), 404
    return render_template('404.html', message="Page not found"), 404


@err_handler_bp.errorhandler(500)
def internal_error(error):
    # Return JSON for API requests, HTML for regular requests
    if request.path.startswith('/api/'):
        return jsonify({"error": "Internal server error"}), 500
    return render_template('500.html', message="Internal server error"), 500
