#!/usr/bin/python3
"""
app
"""

from flask import Flask
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
    app.run(getenv("HBNB_API_HOST"), getenv("HBNB_API_PORT"))
