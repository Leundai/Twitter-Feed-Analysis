import os
from dotenv import load_dotenv

# Set base directory of the app
basedir = os.path.abspath(os.path.dirname(__file__))

# Load the .env and .flaskenv variables
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    """
    Set the config variables for the Flask app

    """

    # Example
    SECRET_KEY = os.environ.get("SECRET_KEY")

    user = os.environ.get("MONGO_USER")
    password = os.environ.get("MONGO_PASSWORD")
    db = os.environ.get("MONGO_DB")
    host = os.environ.get("MONGO_HOST")
    MONGODB_URI = host % (user, password, db)
    MONGODB_SETTINGS = {"db": db, "host": MONGODB_URI}

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

    REDIS_URL = os.environ.get("REDIS_URL") or "redis://"

    TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY")
    TWITTER_API_SECRET = os.environ.get("TWITTER_API_SECRET")
    TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_SECRET = os.environ.get("TWITTER_ACCESS_SECRET")
    TWITTER_BEARER = os.environ.get("TWITTER_BEARER")

    secret_key = os.environ.get("AUTHLIB_SECRET_KEY")
