import os
import logging
from config_flask import Config

from flask import Flask, session
from flask_cors import CORS
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mongoengine import MongoEngine
from authlib.integrations.flask_client import OAuth

from api.core import all_exception_handler

from redis import Redis
import rq

from logging.handlers import RotatingFileHandler

db = MongoEngine()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=os.environ.get("REDIS_URL"),
    strategy="fixed-window",
)
oauth = OAuth()

from transformers import pipeline

emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None,
)


# why we use application factories http://flask.pocoo.org/docs/1.0/patterns/appfactories/#app-factories
def create_app(config_class=Config):
    """
    The flask application factory. To run the app somewhere else you can:
    ```
    from api import create_app

    app = create_app()

    if __name__ == "__main__":
        app.run()
    ```
    """

    app = Flask(__name__)
    app.config.from_object(config_class)
    app.secret_key = "POTATOES"
    app.redis = Redis.from_url(app.config.get("REDIS_URL", "redis://"))
    app.task_queue = rq.Queue("flask-api-queue", connection=app.redis)
    oauth.register(
        name="twitter",
        client_id=app.config.get("TWITTER_API_KEY"),
        client_secret=app.config.get("TWITTER_API_SECRET"),
        api_base_url="https://api.twitter.com/1.1/",
        request_token_url="https://api.twitter.com/oauth/request_token",
        access_token_url="https://api.twitter.com/oauth/access_token",
        authorize_url="https://api.twitter.com/oauth/authenticate",
        fetch_token=lambda: session.get("token"),  # DON'T DO IT IN PRODUCTION
    )

    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db, compare_type=True)

        jwt.init_app(app)
        cors.init_app(app)
        limiter.init_app(app)

        oauth.init_app(app)

    # import and register blueprints
    from api.views.main import bp as main_bp
    from api.views.app_blueprint import bp as app_blueprint_bp
    from api.views.auth import bp as auth_bp

    # why blueprints http://flask.pocoo.org/docs/1.0/blueprints/
    app.register_blueprint(app_blueprint_bp)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(main_bp, url_prefix="/api")

    # Set the rate limit for all routes in the auth_bp blueprint to 1 per second
    # Example: limiter.limit("60 per minute")(main.main)

    if not app.debug:
        if not os.path.exists("logs"):
            os.mkdir("logs")
        file_handler = RotatingFileHandler(
            "logs/flask_api.log", maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
            )
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("Flask API startup")

    app.register_error_handler(Exception, all_exception_handler)

    return app
