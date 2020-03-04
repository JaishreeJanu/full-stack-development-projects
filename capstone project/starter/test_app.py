import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie, db_insert_records
from config import bearer_tokens
from sqlalchemy import desc
from datetime import date

assistant_auth =   {
                    "Authorization": bearer_tokens["casting_assistant"]
                    }
director_auth_header =  {
                            "Authorization": bearer_tokens["casting_director"]
                        }
producer_auth_header = {
                            "Authorization": bearer_tokens["executive_producer"]
                        }

new_actor = {"name": "ryan gosling", "age": 35, "gender": "Male"}
new_movie = {"title": "Lagaan", "release_date": date.today()}


class CastingTestCase(unittest.TestCase):
    def setUp(self):

        self.app = create_app()
        self.client = self.app.test_client
        database_path = os.environ["DATABASE_URL"]
        setup_db(self.app, database_path)
        # binds the app to the current context

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    # tests for POST /actors

    def test_add_actor(self):
        # add new actors: success scenario
        res = self.client().post(
            "/actors", json=new_actor, headers=director_auth_header
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["actor"], 2)

    def test_add_actor_401(self):
        # add new actor: failure ,without authorization header
        res = self.client().post("/actors", json=new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Authorization header is expected.")

    def test_add_actor_400(self):
        # add new actor: failure , without 'name' in json
        this_actor = {"age": 45}
        res = self.client().post(
            "/actors", json=this_actor, headers=director_auth_header
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], 'Please add "name" in the json')

    # tests for GET /actors
    def test_get_actors(self):
        # get actors at page=1
        res = self.client().get("/actors?page=1", headers=assistant_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(len(data["actors"]), 2)

    def test_get_actors_404(self):
        # get actors at page=100
        res = self.client().get("/actors?page=100", headers=assistant_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "OOPS! No actors willing to work")

    def test_get_actors_401(self):
        # get actors: failure ,without authorization header
        res = self.client().get("/actors")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Authorization header is expected.")

    # tests for PATCH /actors
    def test_modify_actors(self):
        # update an actor , sending id and json
        this_actor = {"name": "Priyanka Chopra"}
        res = self.client().patch(
            "/actors/1", json=this_actor, headers=producer_auth_header
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["actor"], 1)

    def test_modify_actors_400(self):
        # update an actor , not sending json
        res = self.client().patch("/actors/1", headers=producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "there is no json body")

    def test_modify_actors_403(self):
        # update an actor ,sending assistant header(doesn't contain required permissions)
        this_actor = {"name": "Priyanka Chopra"}
        res = self.client().patch("/actors/1", json=this_actor, headers=assistant_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Permission not found.")

    # tests for DELETE /actors
    def test_delete_actor_404(self):
        # delete an actor , failure scenario: incorrect actor_id
        res = self.client().delete("/actors/10", headers=producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "No actor with this id")

    def test_delete_actor_401(self):
        # delete an actor , without headers
        res = self.client().delete("/actors/1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Authorization header is expected.")

    def test_delete_actor(self):
        # delete an actor:success scenario
        res = self.client().delete("/actors/1", headers=producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["actor"], 1)

    # tests for POST /movies

    def test_add_movie(self):
        # add new movies: success scenario
        res = self.client().post(
            "/movies", json=new_movie, headers=producer_auth_header
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["movie"], 2)

    def test_add_movie_401(self):
        # add new movie: failure ,without authorization header
        res = self.client().post("/movies", json=new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Authorization header is expected.")

    def test_add_movie_400(self):
        # add new actor: failure , without json
        res = self.client().post("/movies", headers=producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "there is no json body")

    # tests for GET /movies
    def test_get_movies(self):
        # get movies at page=1
        res = self.client().get("/movies?page=1", headers=assistant_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(len(data["movies"]), 2)

    def test_get_movies_404(self):
        # get movies at page=100
        res = self.client().get("/movies?page=100", headers=assistant_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "OOPS! No one is making movies")

    def test_get_movies_401(self):
        # get movies: failure ,without authorization header
        res = self.client().get("/movies")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Authorization header is expected.")

    # tests for PATCH /movies
    def test_modify_movies(self):
        # update an movie , sending id and json
        this_movie = {"title": "mahabharta"}
        res = self.client().patch(
            "/movies/1", json=this_movie, headers=producer_auth_header
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["movie"], 1)

    def test_modify_movies_400(self):
        # update an movie , not sending json
        res = self.client().patch("/movies/1", headers=producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "there is no json body")

    def test_modify_movies_403(self):
        # update an movie , sending assistant header
        this_movie = {"title": "mahabharta"}
        res = self.client().patch("/movies/1", json=this_movie, headers=assistant_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Permission not found.")

    # tests for DELETE /movies
    def test_delete_movie_404(self):
        # delete an movie , failure scenario: incorrect movie_id
        res = self.client().delete("/movies/10", headers=producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "No movie with this id")

    def test_delete_movie_403(self):
        # delete an actor , failure senario, sending director header
        res = self.client().delete("/movies/1", headers=director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Permission not found.")

    def test_delete_movie(self):
        # delete an movie:success scenario
        res = self.client().delete("/movies/1", headers=producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["movie"], 1)


if __name__ == "__main__":
    unittest.main()
