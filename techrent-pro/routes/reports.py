
from flask import (
    Blueprint, jsonify, redirect, render_template, request, url_for
)
from utils.pagination import Paginator

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")


@reports_bp.route('/')
def reports():
    return render_template('reports/index.html')
