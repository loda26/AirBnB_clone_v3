#!/usr/bin/python3
"""
app
"""

from flask import Flask, jsonify
from os import getenv
from api.v1.views import app_views
from models import storage


app = Flask(__name__)


app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    teardown function
    """
    storage.close()


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
