from flask import Blueprint

bp = Blueprint("auth", __name__)  # initialize blueprint

from api.views.auth import routes
