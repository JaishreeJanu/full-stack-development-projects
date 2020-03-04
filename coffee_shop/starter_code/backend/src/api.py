import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)
db_drop_and_create_all()

## ROUTES


@app.route("/drinks", methods=["GET"])
def get_drinks_menu():
    """should get only brief description of the drink
    Returns:
        status code 200 and json {"success": True, "drinks": list_of_drinks}
    """
    drink_results = Drink.query.all()
    drinks = [Drink.short(drink) for drink in drink_results]

    return jsonify({"success": True, "drinks": drinks}), 200


@app.route("/drinks-detail")
@requires_auth("get:drinks-detail")
def get_drinks_detail(token):
    """it should require the 'get:drinks-detail' permission
    it should contain the drink.long() data representation
    Returns:
        status code 200 and json {"success": True, "drinks": list_of_drinks}
    """
    drink_results = Drink.query.all()
    drinks = [Drink.long(drink) for drink in drink_results]
    return jsonify({"success": True, "drinks": drinks}), 200

@app.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def create_drink(token):
    """ it should create a new row in the drinks table
    it should require the 'post:drinks' permission
    it should contain the drink.long() data representation
    Returns:
        status code 200 and json {"success": True, "drinks": new_drink}
    """
    body = json.loads(request.data.decode("utf-8"))
    new_drink = Drink(title=body["title"], recipe=json.dumps(body["recipe"]))
    Drink.insert(new_drink)

    return jsonify({"success": True, "drinks": Drink.long(new_drink)}), 200


@app.route("/drinks/<int:drink_id>", methods=["PATCH"])
@requires_auth("patch:drinks")
def update_drink(token, drink_id):
    """
    it should respond with a 404 error if <id> is not found
    it should update the corresponding row for <id>
    it should require the 'patch:drinks' permission
    it should contain the drink.long() data representation
    Arguments:
        drink_id {int}: drink id
    Returns:
        status code 200 and json {"success": True, "drinks": updated_drink}
    """
    data = json.loads(request.data.decode("utf-8"))
    this_drink = Drink.query.get(drink_id)
    if not this_drink:
        abort(404)

    if "title" in data:
        this_drink.title = data["title"]

    if "recipe" in data:
        this_drink.recipe = data["recipe"]

    Drink.update(this_drink)

    return jsonify({"success": True, "drinks": Drink.long(this_drink)}), 200


@app.route("/drinks/<int:drink_id>", methods=["DELETE"])
@requires_auth("delete:drinks")
def delete_drink(token, drink_id):
    """it should respond with a 404 error if <id> is not found
    it should delete the corresponding row for <id>
    it should require the 'delete:drinks' permission
    
    Arguments:
        token {string} -- token
        drink_id {[=int} -- drink id
    
    Returns:
        json -- {"success": True, "delete": id}
    """
    drink = Drink.query.get(drink_id)
    Drink.delete(drink)

    return jsonify({"success": True, "delete": drink_id}), 200


## Error Handling


@app.errorhandler(422)
def unprocessable(error):
    return (
        jsonify({"success": False, "error": 422, "message": "unprocessable"}),
        422,
    )
@app.errorhandler(404)
def resouce_not_found(error):
    return (
        jsonify({"success": False, "error": 404, "message": "resource not found"}),
        404,
    )


"""implement error handler for AuthError
error handler should conform to general task above 
"""

@app.errorhandler(AuthError)
def authentification_failed(error):
    return jsonify(
        {"success": False, "error": error.status_code, "message": error.error}
    )