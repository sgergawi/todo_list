from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user


homepage = Blueprint('homepage', __name__)


@homepage.route('/main')
@jwt_required(fresh=True)
def logged():
    return render_template('index.html', email=current_user.email)


@homepage.route('/')
def unlogged():
    return render_template('unlogged.html')
