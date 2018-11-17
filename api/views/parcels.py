from flask import Blueprint, jsonify, request
from api.models.models import parcels
from api.models.senditdb import DatabaseConnection
from api.validations import Validation
from api.Handlers.error_handlers import InvalidUsage
from functools import wraps
import datetime


db = DatabaseConnection()
val = Validation()


parcel_blueprint = Blueprint("parcel", __name__)


@parcel_blueprint.route('/api/v1/parcel', methods=['POST'], strict_slashes=False)
#@token_req
def create_parcel():

    if request.content_type != "application/json":
        raise InvalidUsage("Invalid content type", 400)
    data = request.get_json()
    parcel_location = data.get('parcel_location')
    parcel_destination = data.get('parcel_destination')
    parcel_weight = data.get('parcel_weight')
    parcel_description = data.get('parcel_description')
    status = data.get('status')

    val_data = val.empty_order_fields(parcel_location, parcel_destination, parcel_weight, parcel_description, status)
    if val_data:
        raise InvalidUsage(val, 400)
    input_type = val.invalid_input_types(parcel_location, parcel_destination, parcel_weight, parcel_description, status)
    if input_type:
        raise InvalidUsage(input_type, 400)
    empty_strings = val.empty_strings_add_weight(parcel_location, parcel_destination, parcel_weight, parcel_description,
                                                 status)
    if empty_strings:
        raise InvalidUsage(empty_strings, 400)

    db.insert_new_parcel(parcel_location, parcel_destination, parcel_weight, parcel_description, status)
    return jsonify({'message': "parcel with description {} has been added".format(parcel_description)}), 201


@parcel_blueprint.route('/api/v1/parcel', methods=['GET'], strict_slashes=False)
#@token_req
def get_all_parcel():

    par = db.get_all_parcels()
    return jsonify({"parcel": par})


@parcel_blueprint.route('/api/v1/parcel/<int:parcel_id>', methods=['GET'], strict_slashes=False)
#@token_req
def get_single_parcel(parcel_id):
    single_parcel = db.get_one_parcel(parcel_id)
    if not single_parcel:
        return jsonify({"message": "parcel does not exist"}), 404
    return jsonify({"single_parcel": single_parcel})


@parcel_blueprint.route('/api/v1/parcel/<int:parcel_id>/cancel', methods=['PUT'], strict_slashes=False)
#@token_req
def cancel_parcel(parcel_id):
    single_parcel = db.get_one_parcel(parcel_id)
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