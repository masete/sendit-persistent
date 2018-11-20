from flask import Blueprint, jsonify, request
from api.models.models import Users
from api.models.senditdb import DatabaseConnection
from api.validations import Validation
from api.Handlers.error_handlers import InvalidUsage
from flask_jwt_extended import (jwt_required, get_jwt_identity)

db = DatabaseConnection()
val = Validation()


parcel_blueprint = Blueprint("parcel", __name__)


@parcel_blueprint.route('/api/v1/parcel', methods=['POST'], strict_slashes=False)
@jwt_required
def create_parcel():

    user_id = get_jwt_identity()

    if not Users.is_admin(user_id):
        return jsonify({"message": "your not authorised"}), 401

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
        raise InvalidUsage('some fields were left blank', 400)
    input_type = val.invalid_input_types(parcel_location, parcel_destination, parcel_weight, parcel_description, status)
    if input_type:
        raise InvalidUsage(input_type, 400)
    empty_strings = val.empty_strings_add_weight(parcel_location, parcel_destination, parcel_weight, parcel_description,
                                                 status)
    if empty_strings:
        raise InvalidUsage(empty_strings, 400)

    db.insert_new_parcel(user_id, parcel_location, parcel_destination, parcel_weight, parcel_description, status)
    return jsonify({'message': "parcel with description {} has been added".format(parcel_description)}), 201


@parcel_blueprint.route('/api/v1/parcel', methods=['GET'], strict_slashes=False)
@jwt_required
def get_all_parcel():
    user_id = get_jwt_identity()

    if not Users.is_admin(user_id):
        return jsonify({"message": "your not authorised"}), 401

    par = db.get_all_parcels()
    return jsonify({"parcel": par})


@parcel_blueprint.route('/api/v1/parcel/<int:parcel_id>', methods=['GET'], strict_slashes=False)
@jwt_required
def get_single_parcel(parcel_id):
    user_id = get_jwt_identity()

    if not Users.is_admin(user_id):
        return jsonify({"message": "your not authorised"}), 401

    single_parcel = db.get_one_parcel(parcel_id)
    if not single_parcel:
        return jsonify({"message": "parcel does not exist"}), 404
    return jsonify({"single_parcel": single_parcel})


@parcel_blueprint.route('/api/v1/parcel/<int:parcel_id>/cancel', methods=['PUT'], strict_slashes=False)
@jwt_required
def cancel_parcel(parcel_id):
    user_id = get_jwt_identity()

    if not Users.is_admin(user_id):
        return jsonify({"message": "your not authorised"}), 401
    if not db.cancel_parcel(parcel_id):
        return jsonify({"message": "parcel does not exist"}), 404
    return jsonify({"message": db.cancel_parcel(parcel_id)})


@parcel_blueprint.route('/api/v1/users/<int:user_id>/parcel', methods=['GET'], strict_slashes=False)
@jwt_required
def get_parcel_by_user_id(user_id):
    user_id = get_jwt_identity()

    if not Users.is_admin(user_id):
        return jsonify({"message": "your not authorised"}), 401
    result = db.find_parcel_by_user_id(user_id)
    if result:
        return jsonify({"message": result})
    return jsonify({"message": "user should post some parcels here, Thanks"})


@parcel_blueprint.route('/api/v1/parcels/<int:parcel_id>/destination', methods=['PUT'], strict_slashes=False)
@jwt_required
def change_destination(parcel_id):
    user_id = get_jwt_identity()

    if not Users.is_admin(user_id):
        return jsonify({"message": "your not authorised"}), 401
    data = request.get_json()
    parcel_destination = data.get('parcel_destination')
    parcel = db.change_destination(parcel_destination, parcel_id)
    return jsonify({"parcel": parcel})


@parcel_blueprint.errorhandler(InvalidUsage)
@jwt_required
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response