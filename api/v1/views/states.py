#!/usr/bin/python3
"""
route for handling State objects and operations
"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import State


@app_views.route('/states', methods=["Get"], strict_slashes=False)
def get_all_states():
    """
    retrieves all State objects
    :return: json of all states
    """
    state_list = []
    state_obj = storage.all("State")
    for obj in state_obj:
        state_list.append(obj.to_json())
    return 


@app_views.route('/states/<state_id>', strict_slashes=False)
def get_state(state_id):
    """
    gets a specific State object by ID
    :param state_id: state object id
    :return: state obj with the specified id or error
    """
    state_obj = storage.get(State, state_id)

    if state_obj:
        return jsonify(state_obj.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', method=['Delete'], strict_slashes=False)
def delete_state(state_id):
    """
    deletes State by id
    :param state_id: state object id
    :return: empty dict with 200 or 404 if not found
    """
    state_obj = storage.get(State, state_id)

    if state_obj:
        storage.delete(state_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', method=['Post'], strict_slashes=False)
def create_state():
    """
    create state route
    :return: newly created state obj
    """
    state_json = request.get_json(silent=True)

    if state_json is None:
        abort(400, 'Not a Json')
    if "name" not in state_json:
        abort(400, 'Missing Name')

    new_state = State(**state_json)
    result = jsonify(new_state.to_json())
    result.status_code = 201

    return result


@app_views.route('/states/<state_id>', method=['Put'], strict_slashes=False)
def update_state(state_id):
    """
    updates specific State object by ID
    :param state_id: state object ID
    :return: state object and 200 on success, or 400 or 404 on failure
    """
    state_json = request.get_json(silent=True)

    if state_json is None:
        abort(404, 'Not a Json')
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    for key, val in state_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state_obj, key, val)
    state_obj.save()
    return jsonify(state_obj.to_json())
