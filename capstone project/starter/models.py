import os
from sqlalchemy import Column, String, Integer, create_engine, Date
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import date

# database_name = "bollywood"
# database_path = "postgres://{}:{}@{}/{}".format('jaishree','',
# 'localhost:5432',
# database_name)
# database_path = os.environ['DATABASE_URL']
database_path = 'postgres://paxwvjtokrycpn:0d70426e3faaa90c7042d'+
'30305d165ac59aab21f3004ebe3a620361f583b1374'+
'@ec2-3-229-210-93.compute-1.amazonaws.com:5432/d20ktjloq6m7p0'

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.drop_all()
    # db.create_all()
    # db_insert_records()


def db_insert_records():

    # db.create_all()

    new_actor = Actor(name='Gisele Budchen', age=40, gender='Female')
    new_movie = Movie(title="Lessons", release_date=date.today())

    new_actor.insert()
    new_movie.insert()


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(Date, nullable=False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
        }


'''
Actor
'''


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
