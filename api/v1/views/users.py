#!/usr/bin/python3
"""
route for handling User objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_all_users():
    """
    retrieves all user objects
    :return: json of all states
    """
    am_list = []
    for key, value in storage.all(User).items():
        am_list.append(value.to_dict())
    return jsonify(am_list)


@app_views.route("/users/<user_id>",  methods=["GET"],
                 strict_slashes=False)
def get_user(user_id):
    """
    gets a specific user object by ID
    :param user_id: user object id
    :return: state obj with the specified id or error
    """
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        return abort(404)
    else:
        return jsonify(user_obj.to_dict())


@app_views.route("/users/<user_id>",  methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """
    deletes user by id
    :param user_id: user object id
    :return: empty dict with 200 or 404 if not found
    """
    fetched_obj = storage.get(User, user_id)

    if fetched_obj is None:
        return abort(404)
    else:
        storage.delete(fetched_obj)
        storage.save()
        return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """
    create user route
    :return: newly created user obj
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    user_json = request.get_json()
    if user_json is None:
        return abort(400, 'Not a JSON')
    if 'name' not in user_json:
        return abort(400, 'Missing name')

    new_user = User(**user_json)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>",  methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """
    updates specific user object by ID
    :param user_id: user object ID
    :return: user object and 200 on success, or 400 or 404 on failure
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    user_json = request.get_json()
    if user_json is None:
        return abort(400, 'Not a JSON')
    fetched_obj = storage.get(User, user_id)
    if fetched_obj is None:
        return abort(404)
    for key, value in user_json.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(fetched_obj, key, value)
    fetched_obj.save()
    return jsonify(fetched_obj.to_dict()), 200
