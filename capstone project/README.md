# Capstone Project of FSND: Casting Agency

## Motivation
The motivation behind creating this project is to apply the skills learnt during Full stack Nanodegree program.
Following topics, libraries and skills learnt as part of this program:
1. SQL and database modeling for the web ```(SQL, flask-sqlalchemy, flask-migrate)```
2. API development and documentation ```(flask, unittest)```
3. Identity and access management ```(Auth0)```
4. Server deployment, Containerization and testing ```(docker and kubernetes)```


This app has been deployed on heroku:
[URL of this app](https://final-capstone-udacity.herokuapp.com/actors)


## Project dependencies, local development and hosting instructions

1. First cd into the project folder
2. Install [python](https://www.python.org/downloads/) and [postgres](https://www.postgresql.org/download/).
3. Initialize a virtual environment:
```
$ virtualenv --no-site-packages env
$ source env/scripts/activate
``` 
4. Install the dependencies:
```
pip3 install requirements.txt
```
5. Setup database in ```models.py ```:
```
database_path = "postgres://{}:{}@{}/{}".format(<user-name>,'<password>','localhost:5432', <database_name>)
```

6. Setup Auth0:
 > create an account on auth0
 > Create an application  <casting-agency>
 > Create an API <castings>
 > Define permissions in API. Following permissions defined :
 ``` 
 read:actors, read:movies, add:actor, add:movie, modify:actor, modify:movie, delete:actor, delete:movie
 ```
 > Define role: Casting assistant, casting director and casting producer 
 > Give permissions to the roles

7. ```export FLASK_APP=app.py
	export FLASK_ENV=development```
8. Now start local development server
```flask run ```

9. All endpoints written in ```app.py```, models in ```models.py```, config variable in ```config.py``` and all dependencies are in ```requirements.txt```
10. To tun the ```test_app.py``` file, execute ```python3 test_app.py```.

## API documentation and RBAC controls

The roles and their permissions have been explained here:
1. Casting assistant has following permissions:
- GET /actors: Can view all actors
- GET /movies: Can view all movies

2. Casting diresctor has all permissions of assistant and other permissions as well:
- PATCH /actors/<actor-id>: Can modify an actor
- PATCH /movies/<movies-id>:Can modify a movie
- DELETE /actors/<actor-id>: Can delete an actor
- POST /actors: Can add a new actor

3. Casting producer hase following additional permissions:
- POST /movies: Can a add movie
- DELETE /movies/<movie-id>: Can delete a movie

All the endpoints and routes of this app have been explained here:

### GET /actors
- Returns a list of all actors and their details :name,age and gender.
- Send the following request with ```Authorization header``` (It contains ```read:actors``` permission)

- Casting assistant, casting director and casting producer have the permission to get actors.
 ```
 https://final-capstone-udacity.herokuapp.com/actors?page=1
 ```
- Gives following response:
```
{
    "actors": [
        {
            "age": 40,
            "gender": "Female",
            "id": 1,
            "name": "Gisele Budchen"
        },
        {
            "age": 60,
            "gender": "Male",
            "id": 3,
            "name": "Alpachinno"
        }
    ],
    "success": true
}
```

### GET /movies
- Returns a list of all movies and details : title and release_date.
- Send the following request with ```Authorization header``` (It contains ```read:movies``` permission)

- Casting assistant, casting director and casting producer have the permission to get movies.
 ```
 https://final-capstone-udacity.herokuapp.com/movies?page=1
 ```
- Gives following response:
```
{
    "movies": [
        {
            "id": 2,
            "release_date": "Tue, 12 Oct 2021 00:00:00 GMT",
            "title": "83"
        },
        {
            "id": 3,
            "release_date": "Tue, 12 Oct 2021 00:00:00 GMT",
            "title": "Chapaak"
        },
        {
            "id": 4,
            "release_date": "Tue, 12 Oct 2021 00:00:00 GMT",
            "title": "Mahabhartha"
        },
        {
            "id": 1,
            "release_date": "Sat, 29 Feb 2020 00:00:00 GMT",
            "title": "Based on gernder roles"
        }
    ],
    "success": true
}
```
### POST /actors
- Add a new actor in the database and return success and the id of newly created record.
- Send following json in the body:
```
{
	"name":"Anny Hathway",
	"age":32,
	"gender": "Female"
	
}
```
- Also send the token which has ```add:actor``` permission. Casting director and Casting producer have the permission to do so.
- Send a POST request to this url:
```
https://final-capstone-udacity.herokuapp.com/actors
```
- It gives this response:
```
{
    "actor": 4,
    "success": true
}
```
- If request is sent without required permissions , gives this response:
```
{
    "error": 403,
    "message": "Permission not found.",
    "success": false
}
```

### POST /movies
- Add a new movie in the database and return success and the id of newly created record.
- Send following json in the body:
```
{
	"title":"Safe heaven",
	"release_date": "Fri, 24 Apr 2021 00:00:00 GMT"
	
}
```
- Also send the token which has ```add:movie``` permission. Only Casting producer have the permission to do so.
- Send a POST request to this url:
```
https://final-capstone-udacity.herokuapp.com/movies
```
- It gives this response:
```
{
    "movie": 5,
    "success": true
}
```
- If request is sent without required permissions , gives this response:
```
{
    "error": 403,
    "message": "Permission not found.",
    "success": false
}
```
### Patch /actors/<int:actor_id>
- Updates an actor with given id and return success message with id of modified actor.
- Authorization header must have ``` modify:actor ``` permission.
- Send patch request to:
```
https://final-capstone-udacity.herokuapp.com/actors/3
```
- Send request with a json body:
```
{
	"name":"Ranveer singh",
	"gender":"Male"
}
```
- Return following response:
```
{
    "actor": 3,
    "success": true
}
```
- If request is sent without required permission ```modify:actor```
- Gives following response:
```
{
    "error": 403,
    "message": "Permission not found.",
    "success": false
}
```

### Patch /movies/<int:movie_id>
- Updates a movie with given id and return success message with id of modified movie.
- Authorization header must have ``` modify:movie ``` permission.
- Send patch request to:
```
https://final-capstone-udacity.herokuapp.com/movies/1
```
- With JSON body:
```
{
  "title": "Draupadi"
}
```
- Return this reponse
```
{
    "movie": 1,
    "success": true
}
```
- If request is sent without required permission ```modify:actor```
- Gives following response:
```
{
    "error": 403,
    "message": "Permission not found.",
    "success": false
}
```

### DELETE /actors/<actor_id>
- Deletes the given actor record and return success message with the of deleted actor.
- Authorization header should have ``` delete:actor ``` permission.
- Send DELETE request to this url:
```
https://final-capstone-udacity.herokuapp.com/actors/1
```
- Returns this response:
```
{
    "actor": 1,
    "success": true
}
```

### DELETE /movies/<movie_id>
- Deletes the given movie record and return success message with the of deleted movie.
- Authorization header should have ``` delete:movie ``` permission.
- Send DELETE request to this url:
```
https://final-capstone-udacity.herokuapp.com/movies/1
```
- Returns this response:
```
{
    "movie": 1,
    "success": true
}
```
