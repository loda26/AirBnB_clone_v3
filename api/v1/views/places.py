#!/usr/bin/python3
"""
route for handling Place objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """
    retrieves all Place objects by city
    :return: json of all Places
    """
    city_obj = storage.get(City, city_id)
    if not city_obj:
        return abort(404)

    places = [place.to_dict() for place in city_obj.places]
    return jsonify(places)


@app_views.route("/places/<place_id>",  methods=["GET"],
                 strict_slashes=False)
def get_place(place_id):
    """
    gets a specific Place object by ID
    :param place_id: place object id
    :return: place obj with the specified id or error
    """
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        return abort(404)
    else:
        return jsonify(place_obj.to_dict())


@app_views.route("/places/<place_id>",  methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """
    deletes Place by id
    :param place_id: Place object id
    :return: empty dict with 200 or 404 if not found
    """
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        return abort(404)
    else:
        storage.delete(place_obj)
        storage.save()
        return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """
    create place route
    :return: newly created Place obj
    """
    city_obj = storage.get(City, city_id)
    if not city_obj:
        return abort(404)

    city_json = request.get_json()
    if not city_json:
        return abort(404, 'Not a JSON')
    if not storage.get("User", city_json["user_id"]):
        abort(404)
    if 'user_id' not in city_json:
        return abort(400, 'Missing user_id')
    if 'name' not in city_json:
        return abort(400, 'Missing name')

    user_obj = storage.get(User, city_json['user_id'])
    if not user_obj:
        return abort(404)

    city_obj['city_id'] = city_id
    new_place = Place(**city_json)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def place_put(place_id):
    """
    updates specific Place object by ID
    :param place_id: Place object ID
    :return: Place object and 200 on success, or 400 or 404 on failure
    """
    fetched_obj = storage.get(Place, place_id)
    if fetched_obj is None:
        return abort(404)

    place_json = request.get_json()
    if place_json is None:
        abort(400, 'Not a JSON')

    for key, val in place_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    return jsonify(fetched_obj.to_dict()), 200
