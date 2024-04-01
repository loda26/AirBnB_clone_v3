#!/usr/bin/python3
"""
route for handling State objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_city_by_state(state_id):
    """
    retrieves all City objects from a specific state
    :return: json of all cities in a state or 404 on error
    """
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        return abort(404)
    cities = [city.to_dict() for city in state_obj.cities]

    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
def get_city(city_id):
    """
    gets a specific City object by ID
    :param city_id: city object id
    :return: city obj with the specified id or error
    """
    city_obj = storage.get(City, city_id)

    if city_obj is None:
        return abort(404)
    return jsonify(city_obj.to_dict())


@app_views.route("/cities/<city_id>",  methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """
    deletes City by id
    :param city_id: city object id
    :return: empty dict with 200 or 404 if not found
    """
    city_obj = storage.get(City, city_id)

    if city_obj is None:
        return abort(404)
    else:
        storage.delete(city_obj)
        storage.save()
        return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """
    create city route
    param: state_id - state id
    :return: newly created city obj
    """
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        return abort(404)

    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    city_json = request.get_json()
    if city_json is None:
        return abort(400, 'Not a Json')
    if 'name' not in city_json:
        return abort(400, 'Missing name')

    city_json["state_id"] = state_id
    new_city = City(**city_json)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("cities/<city_id>",  methods=["PUT"], strict_slashes=False)
def city_put(city_id):
    """
    updates specific City object by ID
    :param city_id: city object ID
    :return: city object and 200 on success, or 400 or 404 on failure
    """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        return abort(404)

    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    city_json = request.get_json()
    if city_json is None:
        return abort(400, 'Not a JSON')

    for key, vlaue in city_json.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(city_obj, key, vlaue)
    city_obj.save()

    return jsonify(city_obj.to_dict()), 200
