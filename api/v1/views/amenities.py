#!/usr/bin/python3
"""
route for handling Amenity objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_all_amenity():
    """
    retrieves all Amenity objects
    :return: json of all states
    """
    am_list = []
    for key, value in storage.all(Amenity).items():
        am_list.append(value.to_dict())
    return jsonify(am_list)


@app_views.route("/amenities/<amenity_id>",  methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """
    gets a specific Amenity object by ID
    :param amenity_id: amenity object id
    :return: state obj with the specified id or error
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    else:
        return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>",  methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    deletes Amenity by id
    :param amenity_id: Amenity object id
    :return: empty dict with 200 or 404 if not found
    """
    fetched_obj = storage.get(Amenity, amenity_id)

    if fetched_obj is None:
        return abort(404)
    else:
        storage.delete(fetched_obj)
        storage.save()
        return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """
    create amenity route
    :return: newly created amenity obj
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    am_json = request.get_json()
    if am_json is None:
        return abort(400, 'Not a JSON')
    if 'name' not in am_json:
        return abort(400, 'Missing name')

    new_am = Amenity(**am_json)
    new_am.save()
    return jsonify(new_am.to_dict()), 201


@app_views.route("/amenities/<amenity_id>",  methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    updates specific Amenity object by ID
    :param amenity_id: amenity object ID
    :return: amenity object and 200 on success, or 400 or 404 on failure
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    am_json = request.get_json()
    if am_json is None:
        return abort(400, 'Not a JSON')
    fetched_obj = storage.get(Amenity, amenity_id)
    if fetched_obj is None:
        return abort(404)
    for key, value in am_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetched_obj, key, value)
    fetched_obj.save()
    return jsonify(fetched_obj.to_dict()), 200
