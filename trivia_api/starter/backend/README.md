# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Reference
### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.

### Error Handling

Errors are returned as JSON objects in the following format:
```bash
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 422: unprocessable
- 405: Method not allowed

### Endpoints

#### GET /categories
- Returns a list of categories as dictionary and a success value.
- No query parameter and argument
- Sample : 
``` bash
curl http://localhost:5000/categories
```

```bash
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}

#### GET /questions
- Returns a list of questions(list type), number of questions, list of all categories(dictionary type) and success value.
- Results are paginated in groups of 10. Include a request argument to choose page number, default value is 1.
- Returns '404' (resource not found) if there are no questions to serve on the page.
- Sample: ```bash
 curl http://localhost:5000/questions?page=2 
```

```bash
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }
  ], 
  "success": true, 
  "total_questions": 5
}

```

#### DELETE /questions/{question_id}

- Deletes the question of the given ID if it exists. Returns the success value.
- Returns 404 error message if no question with {question_id} found.
Sample: 
```bash
curl -X DELETE http://localhost:5000/questions/17
{
  "success": true
}

```

#### POST /questions 

- Inserts new question, takes argument in json format.
- Return success value and the new inserted question in json form.
- If any of the arguments is null, 400 error(bad request) is returned.
Sample:
```bash
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"What are the mountain ranges in southe germany known as","answer":"alps","category":3,"difficulty":4}'
```

```bash
{
  "question": {
    "answer": "alps", 
    "category": 3, 
    "difficulty": 4, 
    "id": 33, 
    "question": "What are the mountain ranges in southe germany known as"
  }, 
  "success": true
}

Bad request Sample:
```bash
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"What are the mountain ranges in southe germany known as","answer":,"category":3,"difficulty":4}'
{
  "error": 400, 
  "message": "bad request", 
  "success": false
}


#### POST /search

- Search questions for the given search term. 
- Takes JSON arguments: search term
- Returns list of questions , total number of questions in search and success value.
- Return 404 error (resource not found), if no questions are found.
- Sample:
```bash
curl http://127.0.0.1:5000/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"won"}'
```

```bash
{
  "currentCategory": null, 
  "questions": [
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ], 
  "success": true, 
  "totalQuestions": 1
}
```
#### GET /categories/<int:category_id>/questions

- Returns all questions of the given category_id, total number of questions , success value and current category
- Return 404 error, if no questions found for the given category.
- Sample:
```bash
curl http://127.0.0.1:5000/categories/3/questions
``` 

```bash
{
  "current_category": 3, 
  "questions": [
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Rajasthan", 
      "category": 3, 
      "difficulty": 2, 
      "id": 24, 
      "question": "Which state has deserts in India"
    }, 
    {
      "answer": "Europe", 
      "category": 3, 
      "difficulty": 1, 
      "id": 27, 
      "question": "Which continent is Germany located in ?"
    }, 
    {
      "answer": "alps", 
      "category": 3, 
      "difficulty": 4, 
      "id": 33, 
      "question": "What are the mountain ranges in southe germany known as"
    }, 
    {
      "answer": "alps", 
      "category": 3, 
      "difficulty": 4, 
      "id": 34, 
      "question": "What are the mountain ranges in southe germany known as"
    }
  ], 
  "success": true, 
  "total_questions": 5
}

Sample: 404 error
```bash
curl http://127.0.0.1:5000/categories/6/questions
{
  "error": 404, 
  "message": "resource not found", 
  "success": false
}
```

#### POST /quizzes

- Takes two arguments in JSON format: "previous_questions" and "quiz_category" and returns a question from quiz_category not in the previous list.
- Returns success value and the question.
Sample:
```bash
curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[1,2,3,4,5],"quiz_category":{"id":3}}'
{
  "question": {
    "answer": "The Palace of Versailles", 
    "category": 3, 
    "difficulty": 3, 
    "id": 14, 
    "question": "In which royal palace would you find the Hall of Mirrors?"
  }, 
  "success": true
}

```
 
