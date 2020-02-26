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

'''
@TODO uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks',methods=['GET'])
def get_drinks_menu():
    drink_results = Drink.query.all()
    drinks = [Drink.short(drink) for drink in drink_results]

    return jsonify({
        "success":True,
        "drinks":drinks
    }),200


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(token):
    drink_results = Drink.query.all()
    drinks = [Drink.long(drink) for drink in drink_results]

    return jsonify({
        "success":True,
        "drinks":drinks
    }),200

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks',methods=['POST'])
@requires_auth('post:drinks')
def create_drink(token):
    body = json.loads(request.data.decode('utf-8'))
    new_drink = Drink(title=body['title'],recipe=json.dumps(body['recipe']))
    Drink.insert(new_drink)

    return jsonify({
        'success':True,
        'drinks':Drink.long(new_drink)
    }),200


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<int:drink_id>',methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(token,drink_id):
    data = json.loads(request.data.decode('utf-8'))

    this_drink = Drink.query.get(drink_id)

    if 'title' in data:
        this_drink.title =  data['title']

    if 'recipe' in data:
        this_drink.recipe = data['recipe']

    Drink.update(this_drink)

    return jsonify({
        'success':True,
        'drinks':Drink.long(this_drink)
    }),200

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<int:drink_id>',methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(token,drink_id):
    
    drink = Drink.query.get(drink_id)
    Drink.delete(drink)

    return jsonify({
        'success':True,
        'delete':drink_id
    }),200

## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(404)
def resouce_not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''

@app.errorhandler(AuthError)
def authentification_failed(error): 
    return jsonify({
                    "success": False, 
                    "error": error.status_code,
                    "message": error.error
                    })

