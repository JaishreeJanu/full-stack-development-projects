import os
from flask import Flask, request, abort, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, results):
    """Groups results in group of 10 on each page
    Arguments:
        request {int} -- page number
        results {[type]} -- list
    
    Returns:
        list -- list of questions on current page
    """
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [result.format() for result in results]
    current_questions = questions[start:end]
    return current_questions


def create_app(test_config=None):
    """create and configure the app
    Keyword Arguments:
        test_config --(default: {None})
    Returns:
        [type] -- flask app
    """
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={"r/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        """
        set Access-Control-Allow
        """
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,POST,DELETE,PUT,OPTIONS"
        )
        return response

    @app.route("/categories")
    def list_categories():
        """ handle GET requests for all
        available categories
        Returns:
            dictionary: categories
        """
        categories = Category.query.all()
        categories = {category.id: category.type for category in categories}

        return (jsonify({"success": True, "categories": categories}), 200)

    @app.route("/questions")
    def list_questions():
        """ handle GET requests for all
        available questions on current page
        Returns:
            json: questions, categories, number of questions
        """
        questions = Question.query.all()
        current_questions = paginate_questions(request, questions)
        categories = Category.query.all()
        all_categories = {category.id: category.type for category in categories}

        if len(current_questions) == 0:
            abort(404)

        return (
            jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(current_questions),
                    "categories": all_categories,
                }
            ),
            200,
        )

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        """ delete the record from Question model with
        question_id
        Arguments:
            question_id {int} : question id
        Returns:
            json: success value
        """
        question = Question.query.get(question_id)
        if question is None:
            abort(404)
        question.delete()

        return (jsonify({"success": True}), 200)

    @app.route("/questions", methods=["POST"])
    def create_question():
        """ post a new question
        Returns:
            json: success value and new question
        """
        body = request.get_json()

        new_question = body.get("question")
        new_answer = body.get("answer")
        new_category = body.get("category")
        new_difficulty = body.get("difficulty")

        try:
            if not (
                (new_question) and (new_answer) and (new_category) and (new_difficulty)
            ):
                abort(400)
            insert_question = Question(
                question=new_question,
                answer=new_answer,
                category=new_category,
                difficulty=new_difficulty,
            )
            insert_question.insert()

            return jsonify({"success": True, "question": insert_question.format()}), 200
        except:
            abort(422)

    @app.route("/search", methods=["POST"])
    def search_term():
        """ get questions based on search term
        Returns:
            json: questions and number of questions
        """
        body = request.get_json()
        searchTerm = body.get("searchTerm")

        try:
            search_results = Question.query.filter(
                Question.question.ilike("%" + searchTerm + "%")
            ).all()
            current_questions = paginate_questions(request, search_results)
            num_of_questions = len(current_questions)

            if num_of_questions == 0:
                abort(404)

            return (
                jsonify(
                    {
                        "success": True,
                        "questions": current_questions,
                        "totalQuestions": len(current_questions),
                        "currentCategory": None,
                    }
                ),
                200,
            )
        except:
            abort(422)

    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def category_questions(category_id):
        """ get questions of the given category
        category_id
        Arguments:
            category_id {int} : category id
        Returns:
            json: questions, number of questions
        """
        this_questions = Question.query.filter_by(category=category_id).all()
        questions = paginate_questions(request, this_questions)

        if len(this_questions) == 0:
            abort(404)

        return (
            jsonify(
                {
                    "success": True,
                    "questions": questions,
                    "total_questions": len(this_questions),
                    "current_category": category_id,
                }
            ),
            200,
        )

    @app.route("/quizzes", methods=["POST"])
    def play_quiz():
        """ get questions to play quiz
        Arguments:
            json body : previuos question list, category_id
        Returns:
            json: questions
        """
        body = request.get_json()
        previous_questions = body.get("previous_questions")
        quiz_category = body.get("quiz_category")
        quiz_category_id = int(quiz_category["id"])

        question = Question.query.filter(Question.id.notin_(previous_questions))

        if quiz_category_id:
            question = question.filter_by(category=quiz_category_id)

        question = question.first().format()

        return jsonify({"success": True, "question": question}), 200

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "message": "unprocessable", "error": 422}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "message": "bad request", "error": 400}), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify({"success": False, "message": "method not allowed", "error": 405}),
            405,
        )

    return app

