import os
from flask import Flask, request, abort, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request,results):
  page = request.args.get('page',1,type=int)
  start = (page-1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [result.format() for result in results]
  current_questions = questions[start:end]
  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={"r/*": {"origins": "*"}})
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs  ****
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods','GET,POST,DELETE,PUT,OPTIONS')
    return response

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow ****
  '''

  '''
  @TODO: 
  Create an endpoint to handle GET requests ****
  for all available categories.
  '''

  @app.route('/categories')
  def list_categories():
    categories = Category.query.all()
    categories = {category.id: category.type for category in categories}

    return (jsonify({
        'success':True,
        'categories':categories
    }), 200)


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category=???????, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions')
  def list_questions():
    questions = Question.query.all()
    current_questions = paginate_questions(request,questions)
    categories = Category.query.all()
      
    all_categories = {category.id: category.type for category in categories}
      #categories = [category.format() for category in categories]
    
    if len(current_questions) == 0:
      abort(404)

    return (jsonify({
      'success':True,
      'questions':current_questions,
      'total_questions':len(current_questions),
      'categories':all_categories
    }), 200)

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/questions/<int:question_id>',methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.get(question_id)
    if question is None:
      abort(404)
    question.delete()

    return (jsonify({
        'success':True
    }), 200)


  '''
  @TODO: 
  Create an endpoint to POST a new question, ****
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/questions',methods=['POST'])
  def create_question():
    body = request.get_json()
    
    new_question = body.get('question')
    new_answer = body.get('answer')
    new_category = body.get('category')
    new_difficulty = body.get('difficulty')

    try:
      if not((new_question) and (new_answer) and (new_category) and (new_difficulty)):
        abort(400)
      insert_question = Question(question=new_question , answer=new_answer , category=new_category , difficulty=new_difficulty)
      insert_question.insert()

      return jsonify({
        'success':True,
        'question':insert_question.format()
      }),200
    except:
      abort(422)
    

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. ****
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/search',methods=['POST'])
  def search_term():
    body = request.get_json()
    searchTerm = body.get("searchTerm")

    try:
      search_results = Question.query.filter(Question.question.ilike('%'+searchTerm+'%')).all()
      current_questions = paginate_questions(request, search_results)
      num_of_questions = len(current_questions)
      
      if num_of_questions == 0:
        abort(404)
        
      return jsonify({
        'success':True,
        'questions':current_questions,
        'totalQuestions':len(current_questions),
        'currentCategory':None
        }),200
    except:
      abort(422)


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. ****

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<int:category_id>/questions',methods=['GET'])
  def category_questions(category_id):
    this_questions = Question.query.filter_by(category=category_id).all()
    questions = paginate_questions(request, this_questions)

    if len(this_questions) == 0:
      abort(404)

    return (jsonify(
                {
                    "success": True,
                    "questions": questions,
                    "total_questions": len(this_questions),
                    "current_category": category_id,
                }
            ),200,)


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/quizzes',methods=['POST'])
  def play_quiz():
    body = request.get_json()
    previous_questions = body.get("previous_questions")
    quiz_category = body.get("quiz_category")
    quiz_category_id = int(quiz_category["id"])

    question = Question.query.filter(Question.id.notin_(previous_questions))

    if quiz_category_id:
      question = question.filter_by(category=quiz_category_id)

    question = question.first().format()

    return jsonify({"success": True, "question": question }), 200

  '''
  @TODO: 
  Create error handlers for all expected errors ****
  including 404 and 422. 
  '''

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success':False,
      'message':"unprocessable",
      'error':422
    }),422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success':False,
      'message':"bad request",
      'error':400
    }),400

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'success':False,
      'message':"method not allowed",
      'error':405
    }),405
  
  return app

    