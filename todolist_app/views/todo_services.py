from flask import Blueprint
from flask_jwt_extended import jwt_required

todos = Blueprint('todos', __name__)


@todos.route('/todos')
@jwt_required(fresh=True)
def todos_get():
    return []


@todos.route('/todos', methods=["POST"])
@jwt_required(fresh=True)
def todos_post():
    return []


@todos.route('/todos', methods=["PUT"])
@jwt_required(fresh=True)
def todos_put():
    return []


@todos.route('/todos', methods=["DELETE"])
@jwt_required(fresh=True)
def todos_delete():
    return []

