from datetime import datetime
from datetime import timedelta
from datetime import timezone

from flask import Flask, make_response, url_for, redirect
from .views.todo_services import todos
from .views.authentication import authentication
from .views.homepage import homepage
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies, unset_refresh_cookies

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.default')
    # APP_CONFIG_FILE is an env variable with the absolute path
    # to the config file
    app.config.from_envvar('ENVIRONMENT')
    # app.config["variable_name"]

    app.register_blueprint(todos)
    app.register_blueprint(authentication)
    app.register_blueprint(homepage)

    return app


APP = create_app()
jwt = JWTManager(APP)


@APP.after_request
def refresh_expiring_jwts(response):
    try:
        # refresh jwts close to expiration
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(seconds=60))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response


@jwt.user_identity_loader
def get_user(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    return APP.config[jwt_data["sub"]]


@jwt.invalid_token_loader
def invalid_token(callback):
    return invalid_token_callback(callback)


@jwt.expired_token_loader
def expired_token(callback):
    return invalid_token_callback(callback)


def invalid_token_callback(callback):
    # Invalid Fresh/Non-Fresh Access token in auth header
    resp = make_response(redirect(url_for('authentication.login')))
    unset_jwt_cookies(resp)
    unset_refresh_cookies(resp)
    return resp, 302


if __name__ == '__main__':
    APP.run(debug=True)
