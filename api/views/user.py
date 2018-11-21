from flask import Blueprint, jsonify, request
from api.Helpers.error_handlers import InvalidUsage
from api.Helpers.validations import Validation
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta
from api.models.auth import Users
from werkzeug.security import check_password_hash


ke= Users()
val = Validation()
users_obj = Users(username=None, email=None, password=None)

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

    signup_data = ke.signup_user(username, email, password)

    if not signup_data:
        return jsonify({"message": "user already exists"})
    return jsonify({"signedup user": signup_data}), 201


@user_blueprint.route('/api/v1/user', methods=['GET'])
@jwt_required
def get_all_users():
    user = ke.get_all_users()
    return jsonify({"user": user})


@user_blueprint.route('/api/auth/login', methods=['POST'], strict_slashes=False)
def login():

    if request.content_type != "application/json":
        raise InvalidUsage("Invalid content type", 400)
    data = request.get_json()
    username = data['username']
    password = data['password']

    check_user = ke.fetch_user(username, password)

    my_identity=dict(
                user_id=check_user.get('user_id'),
                user_role=check_user.get('role')
            )

    if check_user:
        check_user = users_obj.fetch_user(username, password=password)
        return jsonify({"access_token": create_access_token(identity=my_identity, expires_delta=timedelta
        (hours=3)), "message": "logged in successfully"}), 200
    return jsonify({'message': 'please enter username'})






