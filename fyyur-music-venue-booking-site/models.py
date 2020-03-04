import os
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean, ARRAY
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json


db = SQLAlchemy()

def setup_db(app):
    '''
    binds a flask application and a SQLAlchemy service
    '''
    app.config.from_object('config')
    db = SQLAlchemy(app)
    migrate = Migrate(app,db)
    db.app = app
    db.init_app(app)
    return db

    '''
    drop_all()
    create_all()
    The above two lines drop the database tables and start fresh,
    can be used to initialize a clean database
    ** No need of above to lines, if flask-migrate is used.
    flask_migrate creates versions and automatically creates and updates table schemas.
    '''

# All models, their relationships and properties

'''
An entity to create instances of venues 
where artists perform.
Extends the base SQLAlchemy model
'''

class Venue(db.Model):
    __tablename__ = 'venue'

    id =  Column(Integer, primary_key=True)
    name =  Column(String, nullable=False)
    city =  Column(String(120), nullable=False)
    state =  Column(String(120), nullable=False)
    address =  Column(String(120), nullable=False)
    phone =  Column(String(120), nullable=False)
    image_link =  Column(String(500))
    facebook_link =  Column(String(120))
    website_link = Column(String(500))
    seeking_talent =  Column( Boolean)
    seeking_description = Column(String(100))
    genres =  Column(ARRAY(String(50)), nullable=True)
    shows =  db.relationship('Musicshows', backref='venue', lazy='dynamic')



    def __init__(self, name, genres, address, city, state, phone, website_link, facebook_link, image_link,
                 seeking_talent=False, seeking_description=""):
        self.name = name
        self.genres = genres
        self.address = address
        self.city = city
        self.state = state
        self.phone = phone
        self.website = website_link
        self.facebook_link = facebook_link
        self.seeking_talent = seeking_talent
        self.seeking_description = seeking_description
        self.image_link = image_link

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def short(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def long(self):
        print(self)
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
        }

    def details(self):
        return {
            'id': self.id,
            'name': self.name,
            'genres': self.genres,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'website_link': self.website_link,
            'facebook_link': self.facebook_link,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description,
            'image_link': self.image_link,
        }


'''
An entity to create instances of artists,
the people who perform.
Extends the base SQLAlchemy model
'''
class Artist(db.Model):
    __tablename__ = 'artist'

    id =  Column(Integer, primary_key=True)
    name =  Column(String, nullable=False)
    city =  Column(String(120), nullable=False)
    state =  Column(String(120), nullable=False)
    phone =  Column(String(120), nullable=False)
    image_link =  Column(String(500))
    facebook_link =  Column(String(120))
    website_link =  Column(String(500))
    seeking_venue =  Column(Boolean)
    seeking_description =  Column(String(100))
    genres =  Column(ARRAY(String(50)), nullable=True)
    shows =  db.relationship('Musicshows',backref='artist',lazy='dynamic')

    def __init__(self, name, genres, city, state, phone, image_link, website_link, facebook_link,
                 seeking_venue=False, seeking_description=""):
        self.name = name
        self.genres = genres
        self.city = city
        self.state = state
        self.phone = phone
        self.website_link = website_link
        self.facebook_link = facebook_link
        self.seeking_venue = seeking_venue
        self.seeking_description = seeking_description
        self.image_link = image_link

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def short(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def details(self):
        return {
            'id': self.id,
            'name': self.name,
            'genres': self.genres,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'website_link': self.website_link,
            'facebook_link': self.facebook_link,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
            'image_link': self.image_link,
        }

'''
Musicshows
An entity to create instances of music shows,
new instance of show is created when an artist books a venue.
It has start_time attribute along with venue_id and artist_id.
Extends the base SQLAlchemy model
'''
class Musicshows(db.Model):
    __tablename__ = 'musicshows'

    id = Column(Integer, primary_key=True, autoincrement=True)
    artist_id = Column(Integer, ForeignKey('artist.id'), primary_key=True)
    venue_id =  Column(Integer, ForeignKey('venue.id'), primary_key=True)
    start_time = Column(DateTime(), nullable=False)

    def __init__(self, venue_id, artist_id, start_time):
        self.venue_id = venue_id
        self.artist_id = artist_id
        self.start_time = start_time

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def details(self):
        return {
        'venue_id': self.venue_id,
        'venue_name': self.venue.name,
        'artist_id': self.artist_id,
        'artist_name': self.artist.name,
        'artist_image_link': self.artist.image_link,
        'start_time': self.start_time
        }

    def artist_details(self):
        return {
        'artist_id': self.artist_id,
        'artist_name': self.artist.name,
        'artist_image_link': self.artist.image_link,
        'start_time': self.start_time.strftime("%m/%d/%Y, %H:%M:%S")
        }

    def venue_details(self):
        return {
        'venue_id': self.venue_id,
        'venue_name': self.venue.name,
        'venue_image_link': self.venue.image_link,
        'start_time': self.start_time.strftime("%m/%d/%Y, %H:%M:%S")
        }