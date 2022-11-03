from flask import Blueprint, request
from api.models import (
    UserProfile,
)
from api.core import create_response, logger

main = Blueprint("main", __name__)  # initialize blueprint

# GET request for /accounts/<type>
@main.route("/secret", methods=["GET"])
def get_secret():

    logger.info("Getting Secret")
    return create_response(data={"secret": "Hello"})
