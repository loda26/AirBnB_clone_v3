#!/usr/bin/python3
"""
app
"""

from api.v1.views import app_views
from flask import jsonify

@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """
    function
    """
    data = {
        "status": "OK"
    }

    resp = jsonify(data)
    resp.status_code = 200

    return resp
