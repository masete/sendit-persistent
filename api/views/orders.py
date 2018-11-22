from flask import Blueprint, jsonify, request
from api.models.models import Parcel
from api.Helpers.validations import Validation
from api.Helpers.error_handlers import InvalidUsage
from api.models.auth import Users
from flask_jwt_extended import (jwt_required, get_jwt_identity)

parcel = Parcel()
val = Validation()

parcel_blueprint = Blueprint("parcel", __name__)


@parcel_blueprint.route('/api/v1/parcel', methods=['POST'], strict_slashes=False)
@jwt_required
def create_parcel():
    user_id = get_jwt_identity()

    # if user_id['user_role']:
    #     return jsonify({"message": "your not authorised"}), 401

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

    parcel.insert_new_parcel(user_id['user_id'], parcel_location, parcel_destination, parcel_weight, parcel_description,
                             status)
    return jsonify({'message': "parcel with description {} has been added".format(parcel_description)}), 201


@parcel_blueprint.route('/api/v1/parcel', methods=['GET'], strict_slashes=False)
@jwt_required
def get_all_parcel():
    user_id = get_jwt_identity()

    # if user_id['user_role']:
    #     return jsonify({"message": "your not authorised"}), 401

    par = parcel.get_all_parcels()
    return jsonify({"parcel": par})


@parcel_blueprint.route('/api/v1/parcel/<int:parcel_id>', methods=['GET'], strict_slashes=False)
@jwt_required
def get_single_parcel(parcel_id):
    user_id = get_jwt_identity()

    # if user_id['user_role']:
    #     return jsonify({"message": "your not authorised"}), 401

    single_parcel = parcel.get_parcel_by_parcel_id(parcel_id)
    if not single_parcel:
        return jsonify({"message": "parcel does not exist"}), 404
    return jsonify({"single_parcel": single_parcel}), 200


@parcel_blueprint.route('/api/v1/parcel/<int:parcel_id>/cancel', methods=['PUT'], strict_slashes=False)
@jwt_required
def cancel_parcel(parcel_id):
    user_id = get_jwt_identity()

    # if user_id['user_role']:
    #     return jsonify({"message": "your not authorised"}), 401
    get_parcel = parcel.get_parcel(parcel_id)
    if not get_parcel:
        return jsonify({"message": "parcel does not exist"}), 400

    # ensure the parcel belongs to the user
    if user_id['user_id'] != get_parcel['user_id']:
        return jsonify({"message": "sorry your not allowed to edit this order"}), 401

    result = parcel.cancel_parcel(parcel_id)
    if not result:
        return jsonify({"message": "We were unable to cancel the order. Please try again"}), 500
    return jsonify({"message": result})


@parcel_blueprint.route('/api/v1/users/<int:user_id>/parcel', methods=['GET'], strict_slashes=False)
@jwt_required
def get_parcel_by_user_id(user_id):
    loggedin_user_id = get_jwt_identity()
    print(loggedin_user_id)

    # if not loggedin_user_id['user_role']:
    #     return jsonify({"message": "your not authorised"}), 401

    result = parcel.find_parcel_by_user_id(user_id)
    if result:
        return jsonify({"message": result})

    return jsonify({"message": "No parcels were found for that user"}), 404


@parcel_blueprint.route('/api/v1/parcels/<int:parcel_id>/destination', methods=['PUT'], strict_slashes=False)
@jwt_required
def change_destination(parcel_id):
    user_id = get_jwt_identity()

    parcel1 = parcel.get_parcel_by_parcel_id(parcel_id)
    # ensure that the parcel has the right status
    if parcel1['status'] != "pending":
        return jsonify(
            {"message": "Parcel destination cant be changed because the parcel is '{}'".format(parcel1['status'])}), 400

    # if not user_id['user_role']:
    #     return jsonify({"message": "your not authorised"}), 401

    data = request.get_json()
    parcel_destination = data.get('parcel_destination')
    parcel2 = parcel.change_destination(parcel_destination, parcel_id)
    return jsonify({"parcel": parcel2})


@parcel_blueprint.route('/api/v1/parcels/<int:parcel_id>/status', methods=['PUT'], strict_slashes=False)
@jwt_required
def admin_change_status(parcel_id):
    user_id = get_jwt_identity()

    if not Users(user_id):
        return jsonify({"message": "This operations is only to be done by the admin"})

    data = request.get_json()
    status = data.get('status')
    admin_status = parcel.admin_change_status(parcel_id, user_id, status)
    return jsonify({"message": "parcel status changed successfully", "status changed": admin_status})


@parcel_blueprint.route('/api/v1/parcels/<int:parcel_id>/present_location', methods=['PUT'], strict_slashes=False)
@jwt_required
def admin_change_location(parcel_id):
    user_id = get_jwt_identity()

    if not Users(user_id):
        return jsonify({"message": "This operations is only to be done by the admin"})

    data = request.get_json()
    parcel_location = data.get('parcel_location')
    admin_location = parcel.admin_change_location(parcel_id, user_id, parcel_location)
    return jsonify({"message": "parcel location changed successfully", "data": admin_location})


@parcel_blueprint.errorhandler(InvalidUsage)
@jwt_required
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
