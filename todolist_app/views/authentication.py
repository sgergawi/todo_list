from flask import Blueprint, render_template, make_response, redirect, jsonify, url_for, request, current_app, flash
from werkzeug.security import generate_password_hash, check_password_hash
from todolist_app.models import User
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, set_access_cookies, \
    set_refresh_cookies
from flask_jwt_extended import unset_jwt_cookies

authentication = Blueprint('auth', __name__)


@authentication.route('/login')
def login():
    return render_template('login.html')


@authentication.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    if (not email in current_app.config) or not check_password_hash(current_app.config[email].password, password):
        flash('Email or password incorrect.')
        return redirect(url_for('auth.login'))

    user = User(email, password)
    return assign_access_refresh_tokens(user, url_for('homepage.logged'))


@authentication.route('/signup')
def signup():
    return render_template('signup.html')


@authentication.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    password = request.form.get('password')

    if email in current_app.config:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    current_app.config[email] = User(email, generate_password_hash(password))
    return redirect(url_for('auth.login'))


@authentication.route('/logout')
@jwt_required()
def logout():
    response = make_response(redirect(url_for('homepage.unlogged')), 302)
    unset_jwt_cookies(response)
    return response


def assign_access_refresh_tokens(user, url):
    access_token = create_access_token(identity=user, fresh=True)
    refresh_token = create_refresh_token(identity=user)
    resp = make_response(redirect(url, 302))
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp
