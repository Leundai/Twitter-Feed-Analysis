from flask import Blueprint

bp = Blueprint("main", __name__)  # initialize blueprint

from api.views.main import routes
