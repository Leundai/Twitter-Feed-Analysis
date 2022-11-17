from flask import Blueprint

bp = Blueprint("app_blueprint", __name__)  # initialize blueprint

from api.views.app_blueprint import routes
