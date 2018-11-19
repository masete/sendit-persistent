from flask import Blueprint, jsonify, request
from api.models.models import Users
from api.models.senditdb import DatabaseConnection
from api.validations import Validation
from api.Handlers.error_handlers import InvalidUsage
from werkzeug.security import check_password_hash
#import jwt
from flask import Flask, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from functools import wraps


db = DatabaseConnection()
val = Validation()


user_blueprint = Blueprint("user", __name__)


@user_blueprint.route('/api/auth/signup', methods=['POST'], strict_slashes=False)
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    val_data = val.val_user_signup(username, email, password)
    if val_data:
        return jsonify({"message": val_data})

    signup_data = db.signup(username, email, password)
    return jsonify({"user": signup_data}), 201


@user_blueprint.route('/api/v1/user', methods=['GET'])
@jwt_required
def get_all_users():
    user = db.get_all_users()
    return jsonify({"user": user})


@user_blueprint.route('/api/auth/login', methods=['POST'], strict_slashes=False)
def login():

    if request.content_type != "application/json":
        raise InvalidUsage("Invalid content type", 400)
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    check_user = db.get_user_by_username(username)
    if not check_user:
        return jsonify({"message": "invalid username or password"}), 404
    if check_password_hash(check_user[3], password):

        # Identity can be any data that is json serializable
        access_token = create_access_token(identity=username, expires_delta=timedelta(hours=3))
        return jsonify(access_token=access_token, message="you have successfully logged in"), 200

