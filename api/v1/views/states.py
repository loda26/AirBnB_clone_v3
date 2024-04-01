#!/usr/bin/python3
"""
Method HTTP for States
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """ Function that retrieves the list of all State """
    all_states = []
    for state in storage.all(State).values():
        all_states.append(state.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Function that retrieves a State
    """
    state_obj = storage.get(State, state_id)
    if state_obj:
        return jsonify(state_obj.to_dict())
    else:
        return abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Function that deletes a state
    """
    state_obj = storage.get(State, state_id)
    if state_obj:
        storage.delete(state_obj)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_state():
    """
    Function that create a state
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')

    state_json = request.get_json()
    if state_json is None:
        return abort(400, 'Not a JSON')

    if 'name' not in state_json:
        abort(400, 'Missing name')

    new_state = State(**state_json)
    new_state.save()

    return jsonify(new_state.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """
    Function that update a state
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')

    state = storage.get(State, state_id)
    if state is None:
        return abort(404)

    state_json = request.get_json()

    if state_json is None:
        abort(400, "Not a JSON")

    for key, value in state_json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()

    return jsonify(state.to_dict()), 200
