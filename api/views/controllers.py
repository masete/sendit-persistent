from flask import Blueprint, jsonify, request
from api.models.models import Parcel, Users
from api.models.senditdb import DatabaseConnection
from api.validations import empty_order_fields, invalid_input_types, empty_strings_add_weight
from api.Handlers.error_handlers import InvalidUsage
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
from functools import wraps
import datetime


db = DatabaseConnection()


parcel_blueprint = Blueprint("parcel", __name__)
user_blueprint = Blueprint("user", __name__)


#def token_req(end_point):
    #@wraps(end_point)
    #def check(*args, **kwargs):
        #if 'token' in request.headers:
            #tk = request.headers['token']
        #else:
            #return jsonify({'message': 'you should login'})
        #try:
            #jwt.decode(tk, 'masete_nicholas_scretekey')
        #except:
            #return jsonify({'message': 'user not authenticated'})
        #return end_point(*args, **kwargs)
    #return check


@user_blueprint.route('/api/auth/signup', methods=['POST'], strict_slashes=False)
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    signup_data = db.signup(username, password, email)
    return jsonify({"user": signup_data}), 201


#@user_blueprint.route('/api/v1/user', methods=['GET'])
#def get_all_users():
    #if not users_list:
        #return jsonify({"message": "there are no users currently"})
    #return jsonify({"users": users_list})


@user_blueprint.route('/api/auth/login', methods=['POST'], strict_slashes=False)
def login():

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    return jsonify({"message": "successfully logged in"}), 200






    #for user in users_list:
        #if not user['username'] == username:
            #return jsonify({"message": "wrong username"})
        #if not check_password_hash(user['password'], 'password'):
            #return jsonify({"message": "wrong password"})

    #tk = jwt.encode({
        #'username': user['username'],
        #'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    #}, 'masete_nicholas_scretekey')
    #return jsonify({"message": "you are now logged in", 'token': tk.decode('UTF-8')})


#@parcel_blueprint.route('/api/v1/parcel', methods=['POST'], strict_slashes=False)
#@token_req
#def create_parcel():

    #if request.content_type != "application/json":
        #raise InvalidUsage("Invalid content type", 400)
    #data = request.get_json()
    #parcel_location = data.get('parcel_location')
    #parcel_destination = data.get('parcel_destination')
    #parcel_weight = data.get('parcel_weight')
    #parcel_description = data.get('parcel_description')
    #user_id = data.get('user_id')
    #status = data.get('status')

    #val = empty_order_fields(parcel_location, parcel_destination, parcel_weight, parcel_description, user_id, status)
    #if val:
        #raise InvalidUsage(val, 400)
    #input_type = invalid_input_types(parcel_location, parcel_destination, parcel_weight, parcel_description, user_id, status)
    #if input_type:
        #raise InvalidUsage(input_type, 400)
    #empty_strings = empty_strings_add_weight(parcel_location, parcel_destination, parcel_weight, parcel_description, user_id, status)
    #if empty_strings:
        #raise InvalidUsage(empty_strings, 400)

    #order = Parcel(parcel_location, parcel_destination, parcel_weight, parcel_description, user_id, status)
    #parcel_orders.append(order.to_dict() )
    #return jsonify({"message": "parcel successfully added ", "parcel": order.to_dict()}), 201


#@parcel_blueprint.route('/api/v1/parcel', methods=['GET'], strict_slashes=False)
#@token_req
#def get_all_parcel():
    #if not parcel_orders:
        #return jsonify({"message": "List is empty first post"})
    #return jsonify({"parcels": parcel_orders})


#@parcel_blueprint.route('/api/v1/parcel/<int:parcel_id>', methods=['GET'], strict_slashes=False)
#@token_req
#def get_single_parcel(parcel_id):
    #for order in parcel_orders:
        #if order['parcel_id'] == parcel_id:
            #return jsonify({"message": "your request is successfull", "data": order}), 200
    #return jsonify({"message": "there is no parcel requested for"}), 400


#@parcel_blueprint.route('/api/v1/parcel/<int:parcel_id>/cancel', methods=['PUT'], strict_slashes=False)
#@token_req
#def cancel_parcel(parcel_id):
    #for order in parcel_orders:
        #if order['parcel_id'] == parcel_id:
            #order['status'] = 'cancelled'
            #return jsonify(order), 200
    #return jsonify({"message": "the parcel does not exist"}), 400


#@parcel_blueprint.route('/api/v1/users/<int:user_id>/parcel', methods=['GET'], strict_slashes=False)
#@token_req
#def get_parcel_by_user_id(user_id):
    #single = []
    #for order in parcel_orders:
        #if order['user_id'] == user_id:
            #single.append(order)

    #if len(single) > 0:
        #return jsonify(single), 200
    #return jsonify({"message": "there is no such user"}), 400


@parcel_blueprint.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response