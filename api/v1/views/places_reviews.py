#!/usr/bin/python3
"""
route for handling Review objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    """
    retrieves all Review objects by place
    :return: json of all reviews
    """
    review_list = []
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        return abort(404)
    for obj in place_obj.reviews:
        review_list.append(obj.to_dict())
    return jsonify(review_list)


@app_views.route("/reviews/<review_id>",  methods=["GET"],
                 strict_slashes=False)
def get_review_by_id(review_id):
    """
    gets a specific Review object by ID
    :param review_id: place object id
    :return: review obj with the specified id or error
    """
    fetched_obj = storage.get(Review, review_id)
    if fetched_obj is None:
        return abort(404)
    else:
        return jsonify(fetched_obj.to_dict())


@app_views.route("/reviews/<review_id>",  methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """
    deletes Review by id
    :param : Review object id
    :return: empty dict with 200 or 404 if not found
    """
    fetched_obj = storage.get(Review, review_id)

    if fetched_obj is None:
        return abort(404)
    storage.delete(fetched_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def creat_reviewe(place_id):
    """
    create REview route
    :return: newly created Review obj
    """
    review_json = request.get_json()
    if review_json is None:
        return abort(400, 'Not a JSON')
    if not storage.get(Place, place_id):
        return abort(404)
    if not storage.get(User, review_json["user_id"]):
        return abort(404)
    if "user_id" not in review_json:
        return abort(400, 'Missing user_id')
    if "text" not in review_json:
        return abort(400, 'Missing text')

    review_json["place_id"] = place_id
    new_review = Review(**review_json)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>",  methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """
    updates specific Review object by ID
    :param review_id: Review object ID
    :return: Review object and 200 on success, or 400 or 404 on failure
    """
    place_json = request.get_json()

    if place_json is None:
        return abort(400, 'Not a JSON')

    fetched_obj = storage.get(Review, review_id)

    if fetched_obj is None:
        return abort(404)

    for key, val in place_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id",
                       "place_id"]:
            setattr(fetched_obj, key, val)

    fetched_obj.save()

    return jsonify(fetched_obj.to_dict()), 200
