from os import path
from flask import Blueprint
from api.core import create_response

app_blueprint = Blueprint("app_blueprint", __name__)  # initialize blueprint


@app_blueprint.route("/")
def serve():
    return create_response(message="Currently at directory /")
