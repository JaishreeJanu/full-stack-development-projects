#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app,db)

# TODO: connect to a local postgresql database ****

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Musicshows(db.Model):
  __tablename__ = 'musicshows'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), primary_key=True)
  start_time = db.Column(db.DateTime(), nullable=False)


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(100))
    genres = db.Column(db.ARRAY(db.String(50)), nullable=True)
    shows = db.relationship('Musicshows', backref='venue', lazy='dynamic')


    # TODO: implement any missing fields, as a database migration using Flask-Migrate ****

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(100))
    genres = db.Column(db.ARRAY(db.String(50)), nullable=True)
    shows = db.relationship('Musicshows',backref='artist',lazy='dynamic')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate ****


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration. ****

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime



#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue. ****
  
  current_time = datetime.now()
  data = []
  venue_city_state = db.session.query(Venue.city,Venue.state).group_by(Venue.city,Venue.state).all()
  i=0

  for v in venue_city_state:
    venue_data = db.session.query(Venue).filter(Venue.city == v.city,Venue.state==v.state).all()
    data.append({
      "city": v.city,
      "state": v.state,
      "venues":[]
    })
    for each_venue in venue_data:
      upcoming_shows = db.session.query(Musicshows).filter(Musicshows.venue_id == each_venue.id,Musicshows.start_time > current_time).count()
      data[i]["venues"].append({
        "id":each_venue.id,
        "name":each_venue.name,
        "num_upcoming_shows":upcoming_shows
      })
    i+=1

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive. ****
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  search_term = request.form['search_term']
  search_results = db.session.query(Venue).filter(Venue.name.ilike('%'+search_term+'%'))
  
  response={
    "count":search_results.count(),
    "data":[]
  }
  for result in search_results:
    num_upcoming_shows = db.session.query(Musicshows).filter(Musicshows.venue_id == result.id,Musicshows.start_time > datetime.now()).count()
    response["data"].append({
      "id":result.id,
      "name":result.name,
      "num_upcoming_shows":num_upcoming_shows
    })
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id ****
  
  data = Venue.query.get(venue_id)
  venue_data=[]
  current_time = datetime.now()

  if data:
    past_results = db.session.query(Musicshows.artist_id,Musicshows.start_time).filter(Musicshows.venue_id==venue_id).filter(Musicshows.start_time < current_time).all()
    upcoming_results = db.session.query(Musicshows.artist_id,Musicshows.start_time).filter(Musicshows.venue_id==venue_id).filter(Musicshows.start_time > current_time).all()

    venue_data.append({
      "id":data.id,
      "name":data.name,
      "city":data.city,
      "state":data.state,
      "address":data.address,
      "genres":data.genres,
      "phone":data.phone,
      "website_link":data.website_link,
      "facebook_link":data.facebook_link,
      "seeking_talent":data.seeking_talent,
      "seeking_description":data.seeking_description,
      "image_link":data.image_link,
      "past_shows":[],
      "upcoming_shows":[],
      "past_shows_count":len(past_results),
      "upcoming_shows_count":len(upcoming_results)
    })
    
    for artist_item in past_results:
      artist_details = db.session.query(Artist).filter(Artist.id==artist_item.artist_id).all()
      #this_start_time = db.session.query(Musicshows.start_time).filter(Musicshows.artist_id==artist_item.artist_id,Musicshows.venue_id==venue_id).all()
      this_start_time = artist_item.start_time
      venue_data[0]["past_shows"].append({
        "artist_id":artist_details[0].id,
        "artist_name":artist_details[0].name,
        "artist_image_link":artist_details[0].image_link,
        "start_time":this_start_time.strftime("%m/%d/%Y, %H:%M:%S")
      })

    for artist_item in upcoming_results:
      artist_details = Venue.query.filter(Artist.id==artist_item.artist_id).all()
      #this_start_time = db.session.query(Musicshows.start_time).filter(Musicshows.artist_id==artist_item.artist_id,Musicshows.venue_id==venue_id).all()
      this_start_time = artist_item.start_time
      venue_data[0]["upcoming_shows"].append({
        "artist_id":artist_details[0].id,
        "artist_name":artist_details[0].name,
        "artist_image_link":artist_details[0].image_link,
        "start_time":this_start_time.strftime("%m/%d/%Y, %H:%M:%S")
      })

  data = list(filter(lambda d: d['id'] == venue_id, venue_data))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead        ****
  # TODO: modify data to be the data object returned from db insertion     ****
  #  
  form = VenueForm(request.form)
  if form.is_submitted():
    print ("Form successfully submitted")

  if form.validate_on_submit():
    try:
      new_venue = Venue(name=request.form['name'],
      city=request.form['city'],
      state=request.form['state'],
      address=request.form['address'],
      phone=request.form['phone'],
      facebook_link=request.form['facebook_link'],
      genres=request.form.getlist('genres'),
      image_link=request.form['image_link'],
      website_link=request.form['website_link'],
      seeking_talent=bool(request.form['seeking_talent']),
      seeking_description=request.form['seeking_description']
      )

      db.session.add(new_venue)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully listed!')

    except SQLAlchemyError as e:
      db.session.rollback()
      print(e)
      flash('OOPS!! Venue ' + request.form['name'] + ' was not listed!')
    finally:
      db.session.close()

  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead. ****
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using ****
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  venue_item = Venue.query.get(venue_id)
  try:
    db.session.delete(venue_item)
    db.session.commit()
    flash('Venue item deleted successfully!')
  except:
    db.session.rollback()
    flash('Venue item deletion failed!')
  finally:
    db.session.close()


  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database   ****
  
  data = db.session.query(Artist.id,Artist.name).all()

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive. ****
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  
  search_term = request.form['search_term']
  search_results = db.session.query(Artist).filter(Artist.name.ilike('%'+search_term+'%'))
  
  response={
    "count":search_results.count(),
    "data":[]
  }
  for result in search_results:
    num_upcoming_shows = db.session.query(Musicshows).filter(Musicshows.artist_id == result.id,Musicshows.start_time > datetime.now()).count()
    response["data"].append({
      "id":result.id,
      "name":result.name,
      "num_upcoming_shows":num_upcoming_shows
    })

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id  ****

  data = Artist.query.get(artist_id)
  artist_data=[]
  current_time = datetime.now()

  if data:
    past_results = db.session.query(Musicshows.venue_id,Musicshows.start_time).filter(Musicshows.artist_id==artist_id).filter(Musicshows.start_time < current_time).all()
    upcoming_results = db.session.query(Musicshows.venue_id ,Musicshows.start_time).filter(Musicshows.artist_id==artist_id).filter(Musicshows.start_time > current_time).all()

    artist_data.append({
      "id":data.id,
      "name":data.name,
      "city":data.city,
      "state":data.state,
      "genres":data.genres,
      "phone":data.phone,
      "website_link":data.website_link,
      "facebook_link":data.facebook_link,
      "seeking_venue":data.seeking_venue,
      "seeking_description":data.seeking_description,
      "image_link":data.image_link,
      "past_shows":[],
      "upcoming_shows":[],
      "past_shows_count":len(past_results),
      "upcoming_shows_count":len(upcoming_results)
    })
    
    for venue_item in past_results:
      venue_details = db.session.query(Venue).filter(Venue.id==venue_item.venue_id).all()
      #this_start_time = db.session.query(Musicshows.start_time).filter(Musicshows.venue_id==venue_item.venue_id,Musicshows.artist_id==artist_id).all()
      this_start_time = venue_item.start_time
      artist_data[0]["past_shows"].append({
        "venue_id":venue_details[0].id,
        "venue_name":venue_details[0].name,
        "venue_image_link":venue_details[0].image_link,
        "start_time":this_start_time.strftime("%m/%d/%Y, %H:%M:%S")
      })

    for venue_item in upcoming_results:
      venue_details = Venue.query.filter(Venue.id==venue_item.venue_id).all()
      #this_start_time = db.session.query(Musicshows.start_time).filter(Musicshows.venue_id==venue_item.venue_id,Musicshows.artist_id==artist_id).all()
      this_start_time = venue_item.start_time
      artist_data[0]["upcoming_shows"].append({
        "venue_id":venue_details[0].id,
        "venue_name":venue_details[0].name,
        "venue_image_link":venue_details[0].image_link,
        "start_time":this_start_time.strftime("%m/%d/%Y, %H:%M:%S")
      })

  data = list(filter(lambda d: d['id'] == artist_id, artist_data))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

  artist = Artist.query.get(artist_id)
  if artist:
    form.name.data = artist.name
    form.genres.data = artist.genres
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.website_link.data = artist.website_link
    form.image_link.data = artist.image_link
    form.facebook_link.data = artist.facebook_link
    form.seeking_venue.data = artist.seeking_venue
    form.seeking_description.data = artist.seeking_description
  # TODO: populate form with fields from artist with ID <artist_id>  ****
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  form = ArtistForm(request.form)
  artist = Artist.query.get(artist_id)
  if artist:
    if form.is_submitted():
      print ("Artist edit Form successfully submitted")
    if form.validate():
      print("Form validated")
      try:
        setattr(artist, 'name', request.form['name'])
        setattr(artist, 'genres', request.form.getlist('genres'))
        setattr(artist, 'city', request.form['city'])
        setattr(artist, 'state', request.form['state'])
        setattr(artist, 'phone', request.form['phone'])
        setattr(artist, 'website_link', request.form['website_link'])
        setattr(artist, 'facebook_link', request.form['facebook_link'])
        setattr(artist, 'image_link', request.form['image_link'])
        setattr(artist, 'seeking_description', request.form['seeking_description'])
        setattr(artist, 'seeking_venue', bool(request.form['seeking_venue']))
        db.session.commit()
        flash("Edited Successfully")
        #return redirect(url_for('show_artist', artist_id=artist_id))
      except SQLAlchemyError as e:
        flash("Edit failed!!")
        print(e)
        return render_template('errors/404.html')
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  if venue:
    form.name.data = venue.name
    form.genres.data = venue.genres
    form.address.data = venue.address
    form.city.data = venue.city
    form.state.data = venue.state
    form.phone.data = venue.phone
    form.website_link.data = venue.website_link
    form.facebook_link.data = venue.facebook_link
    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description
    form.image_link.data = venue.image_link
  # TODO: populate form with values from venue with ID <venue_id> ****
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing ****
  # venue record with ID <venue_id> using the new attributes

  form = VenueForm(request.form)
  venue = Venue.query.get(venue_id)
  if venue:
    if form.validate():
      print('Form validated')
      try:
        setattr(venue, 'name', request.form['name'])
        setattr(venue, 'genres', request.form.getlist('genres'))
        setattr(venue, 'city', request.form['city'])
        setattr(venue,'address',request.form['address'])
        setattr(venue, 'state', request.form['state'])
        setattr(venue, 'phone', request.form['phone'])
        setattr(venue, 'facebook_link', request.form['facebook_link'])
        setattr(venue, 'website_link', request.form['website_link'])
        setattr(venue, 'image_link', request.form['image_link'])
        setattr(venue, 'seeking_talent', bool(request.form['seeking_talent']))
        setattr(venue, 'seeking_description', request.form['seeking_description'])
        db.session.commit()
        flash("Edited Successfully")
      except SQLAlchemyError as e:
        flash("Edit failed!!")
        print(e)
        return render_template('errors/404.html')
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Artist record in the db, instead ****
  # TODO: modify data to be the data object returned from db insertion ****


  form = ArtistForm(request.form)
  if form.is_submitted():
    print ("Form successfully submitted")

  if form.validate_on_submit():
    try:
      new_artist = Artist(name=request.form['name'],
      city=request.form['city'],
      state=request.form['state'],
      phone=request.form['phone'],
      facebook_link=request.form['facebook_link'],
      genres=request.form.getlist('genres'),
      image_link=request.form['image_link'],
      website_link=request.form['website_link'],
      seeking_venue=bool(request.form['seeking_venue']),
      seeking_description=request.form['seeking_description']
      )

      db.session.add(new_artist)
      db.session.commit()
      flash('Artist' + request.form['name'] + ' was successfully listed!')

    except SQLAlchemyError as e:
      db.session.rollback()
      print(e)
      flash('OOPS!! Artist ' + request.form['name'] + ' was not listed!')
    finally:
      db.session.close()

  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead. ****
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue. ****
  
  shows_data=[]
  data = db.session.query(Musicshows).all()

  for show in data:
    show_venues = Venue.query.filter(Venue.id == show.venue_id).all()
    show_artists = Artist.query.filter(Artist.id == show.artist_id).all()
    shows_data.append({
      "venue_id":show_venues[0].id,
      "venue_name":show_venues[0].name,
      "artist_id":show_artists[0].id,
      "artist_name":show_artists[0].name,
      "artist_image_link":show_artists[0].image_link,
      "start_time":show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
    })

  return render_template('pages/shows.html', shows=shows_data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead    ****

  form = ShowForm(request.form)
  if form.validate_on_submit():
    try:
      new_show = Musicshows(artist_id=request.form['artist_id'],venue_id=request.form['venue_id'],start_time=request.form['start_time'])
      db.session.add(new_show)
      db.session.commit()
      flash('Show was successfully listed.')
    except SQLAlchemyError as e:
      db.session.rollback()
      print(e)
      flash('An error occurred. Show could not be listed.')

  #on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.    ****
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
