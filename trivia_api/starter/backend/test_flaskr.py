import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            "jaishree", "password", "localhost:5432", "trivia_test"
        )
        setup_db(self.app, self.database_path)

        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            "question": "Which state of India is known as heaven on earth",
            "answer": "Kashmir",
            "difficulty": 3,
            "category": 3,
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(isinstance(data["categories"], dict))

    def test_get_paginated_questions(self):
        res = self.client().get("/questions/page=1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(isinstance(data["categories"], dict))
        self.assertTrue(isinstance(data["questions"], list))
        self.assertEqual(data["total_questions"], 10)

    def test_get_questions_404_error(self):
        res = self.client().get("/questions/page=50")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"], "resource not found")
        self.assertEqual(data["success"], False)

    def test_delete_question(self):
        res = self.client().delete("/questions/28")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 28).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(question, None)

    def test_delete_question_404_error(self):
        res = self.client().delete("/questions/17")
        data = json.loads(res.data)

        self.assertEqual(data["message"], "resource not found")
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_post_question_success(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["question"], self.new_question["question"])
        self.assertEqual(data["answer"], self.new_question["answer"])
        self.assertEqual(data["category"], self.new_question["category"])
        self.assertEqual(data["difficulty"], self.new_question["difficulty"])

    def test_post_question_failure(self):
        insert_question = {
            "question": "new_question",
            "answer": "",
            "category": 2,
            "difficulty": 3,
        }
        res = self.client().post("/questions", json=insert_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_question_search_success(self):
        res = self.client().post("/search", json={"searchTerm": "mirror"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(isinstance(data["questions"], list))
        self.assertEqual(len(data["questions"]), 1)

    def test_question_search_failure(self):
        res = self.client().post("/search", json={"searchTerm": "orange"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_category_question_success(self):
        res = self.client().get("/categories/2/questions")
        data = json.loads(res.data)

        num_questions = Question.query.filter_by(category=2).count()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["total_questions"], num_questions)
        self.assertTrue(isinstance(data["questions"], list))
        self.assertEqual(data["current_category"], 2)

    def test_get_category_question_failure(self):
        res = self.client().get("/categories/8/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_play_quiz(self):
        res = self.client().post(
            "/quizzes",
            json={"previous_questions": [1, 2, 3], "quiz_category": {"id": 2}},
        )
        data = json.loads(res.data)

        question = data["question"]
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(question["id"] not in [1, 2, 3])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
