from os import path
from flask import Blueprint
from api.views.app_blueprint import bp
from api.core import create_response


@bp.route("/")
def serve():
    return create_response(message="Currently at directory /")
