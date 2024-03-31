#!/usr/bin/python3
"""
index
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status():
    """
    status route
    :return: response with json
    """
    data = {
        "status": "OK"
    }

    resp = jsonify(data)
    return resp

@app_views.route('/stats')
def stats():
    """
    stats of all objs route
    :return: json of all objs
    """
    data = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }

    resp = jsonify(data)
    return resp
