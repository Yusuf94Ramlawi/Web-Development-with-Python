from flask import Blueprint, render_template

swagger_bp = Blueprint("swagger", __name__)


@swagger_bp.route('/api-docs/')
def api_docs():
    """
    Render Swagger UI for API exploration and testing.

    Args:
        None

    Returns:
        Response: Rendered Swagger UI page.
    """
    return render_template('swaggerui.html')
