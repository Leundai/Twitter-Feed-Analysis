from flask import current_app, jsonify, url_for, redirect
from flask_cors import cross_origin, CORS
from uuid import uuid4
from api import oauth
from api.views.auth import bp
from api.core import create_response, logger
from api.models import TaskProfile
from authlib.integrations.flask_client import OAuthError


@bp.errorhandler(OAuthError)
def handle_error(error):
    logger.error(error)
    return create_response(message="OAuthError")


@bp.route("/login")
@cross_origin(supports_credentials=True)
def login():
    redirect_uri = url_for("auth.access_token", _external=True)
    logger.info(redirect_uri)
    return oauth.twitter.authorize_redirect(redirect_uri)


@bp.route("/access_token")
@cross_origin(supports_credentials=True)
def access_token():
    token = oauth.twitter.authorize_access_token()

    create_task = False
    try:
        task: TaskProfile = TaskProfile.objects.get(user_id=token.get("user_id", ""))
    except Exception as e:
        logger.error(e)
        create_task = True

    if create_task:
        new_task = TaskProfile()
        new_task.access_token = token.get("oauth_token", "")
        new_task.access_secret = token.get("oauth_token_secret", "")
        new_task.user_id = token.get("user_id", "")
        new_task.save()

    return redirect(
        f"http://localhost:3000/loading/{token.get('user_id', '')}",
        code=302,
    )


@bp.route("/logout")
def logout():
    return create_response(message="Logging out")


# @bp.route("/tweets")
# def list_tweets():
#     url = "statuses/user_timeline.json"
#     params = {"include_rts": 1, "count": 200}
#     prev_id = request.args.get("prev")
#     if prev_id:
#         params["max_id"] = prev_id

#     resp = oauth.twitter.get(url, params=params)
#     tweets = resp.json()
#     return render_template("tweets.html", tweets=tweets)
