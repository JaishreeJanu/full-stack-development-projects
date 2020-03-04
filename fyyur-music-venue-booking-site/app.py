# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import (
    Flask,
    render_template,
    request,
    Response,
    flash,
    redirect,
    url_for,
    abort,
)
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *
from models import setup_db, Musicshows, Venue, Artist

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
import sys

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
db = setup_db(app)

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format="medium"):
    date = dateutil.parser.parse(value)
    if format == "full":
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == "medium":
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters["datetime"] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route("/")
def index():
    return render_template("pages/home.html")


#  Venues
#  ----------------------------------------------------------------


@app.route("/venues")
def venues():
    """Returns venues (grouped by city and state)
    along with number of upcoming shows in each (city, state).
    Returns:
        list of dictionary -- venues
    """
    current_time = datetime.now()
    data = []
    venue_city_state = (
        db.session.query(Venue.city, Venue.state)
        .group_by(Venue.city, Venue.state)
        .all()
    )
    i = 0

    for v in venue_city_state:
        venue_data = (
            db.session.query(Venue)
            .filter(Venue.city == v.city, Venue.state == v.state)
            .all()
        )
        data.append({"city": v.city, "state": v.state, "venues": []})
        for each_venue in venue_data:
            upcoming_shows = (
                db.session.query(Musicshows)
                .filter(
                    Musicshows.venue_id == each_venue.id,
                    Musicshows.start_time > current_time,
                )
                .count()
            )
            data[i]["venues"].append(
                {
                    "id": each_venue.id,
                    "name": each_venue.name,
                    "num_upcoming_shows": upcoming_shows,
                }
            )
        i += 1

    return render_template("pages/venues.html", areas=data)


@app.route("/venues/search", methods=["POST"])
def search_venues():
    """Returns venue results filtered by the search term.
    'search_term' is received in JSON body here.
    Returns:
        dictionary -- venues
    """
    search_term = request.form["search_term"]
    search_results = db.session.query(Venue).filter(
        Venue.name.ilike("%" + search_term + "%")
    )

    response = {"count": search_results.count(), "data": []}
    for result in search_results:
        num_upcoming_shows = (
            db.session.query(Musicshows)
            .filter(
                Musicshows.venue_id == result.id, Musicshows.start_time > datetime.now()
            )
            .count()
        )
        response["data"].append(
            {
                "id": result.id,
                "name": result.name,
                "num_upcoming_shows": num_upcoming_shows,
            }
        )
    return render_template(
        "pages/search_venues.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


@app.route("/venues/<int:venue_id>")
def show_venue(venue_id):
    """returns details of venue with venue_id.
    Arguments:
        venue_id {int} -- venue id
    
    Returns:
        dictionary -- details of venue
    """
    data = Venue.query.get(venue_id)
    venue_data = {}
    current_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    if data:
        past_results = (
            db.session.query(Musicshows)
            .filter(Musicshows.venue_id == venue_id)
            .filter(Musicshows.start_time < current_time)
            .all()
        )
        upcoming_results = (
            db.session.query(Musicshows)
            .filter(Musicshows.venue_id == venue_id)
            .filter(Musicshows.start_time > current_time)
            .all()
        )

        venue_data = Venue.details(data)
        venue_data["past_shows"] = list(map(Musicshows.artist_details, past_results))
        venue_data["upcoming_shows"] = list(
            map(Musicshows.artist_details, upcoming_results)
        )
        venue_data["past_shows_count"] = len(past_results)
        venue_data["upcoming_shows_count"] = len(upcoming_results)

    return render_template("pages/show_venue.html", venue=venue_data)


#  Create Venue
#  ----------------------------------------------------------------


@app.route("/venues/create", methods=["GET"])
def create_venue_form():
    """creates a venue form
    Returns:
        form -- form fields of different data types
    """
    form = VenueForm()
    return render_template("forms/new_venue.html", form=form)


@app.route("/venues/create", methods=["POST"])
def create_venue_submission():
    """insert form data as a new venue record
    """
    form = VenueForm(request.form)
    if form.is_submitted():
        print("Form successfully submitted")

    if form.validate_on_submit():
        try:
            new_venue = Venue(
                name=request.form["name"],
                city=request.form["city"],
                state=request.form["state"],
                address=request.form["address"],
                phone=request.form["phone"],
                facebook_link=request.form["facebook_link"],
                genres=request.form.getlist("genres"),
                image_link=request.form["image_link"],
                website_link=request.form["website_link"],
                seeking_talent=bool(request.form["seeking_talent"]),
                seeking_description=request.form["seeking_description"],
            )

            Venue.insert(new_venue)
            flash("Venue " + request.form["name"] + " was successfully listed!")

        except SQLAlchemyError as e:
            db.session.rollback()
            print(e)
            flash("OOPS!! Venue " + request.form["name"] + " was not listed!")
        finally:
            db.session.close()

    return render_template("pages/home.html")


@app.route("/venues/<venue_id>", methods=["DELETE"])
def delete_venue(venue_id):
    """deletes a record from venue model
    Arguments:
        venue_id {int} -- venue id
    """
    venue_item = Venue.query.get(venue_id)
    try:
        Venue.delete(venue_item)
        flash("Venue item deleted successfully!")
    except:
        db.session.rollback()
        flash("Venue item deletion failed!")
    finally:
        db.session.close()
    return None


#  Artists
#  ----------------------------------------------------------------
@app.route("/artists")
def artists():
    """returns artist names
    Returns:
        list -- artists
    """
    data = db.session.query(Artist.id, Artist.name).all()
    return render_template("pages/artists.html", artists=data)


@app.route("/artists/search", methods=["POST"])
def search_artists():
    """returns search results of artists
    Returns:
        dictionary -- artists
    """

    search_term = request.form["search_term"]
    search_results = db.session.query(Artist).filter(
        Artist.name.ilike("%" + search_term + "%")
    )

    response = {"count": search_results.count(), "data": []}
    for result in search_results:
        num_upcoming_shows = (
            db.session.query(Musicshows)
            .filter(
                Musicshows.artist_id == result.id,
                Musicshows.start_time > datetime.now(),
            )
            .count()
        )
        response["data"].append(
            {
                "id": result.id,
                "name": result.name,
                "num_upcoming_shows": num_upcoming_shows,
            }
        )

    return render_template(
        "pages/search_artists.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


@app.route("/artists/<int:artist_id>")
def show_artist(artist_id):
    """shows artist page with artist details
    Arguments:
        artist_id {int} -- artist id
    Returns:
        dictionary -- artist details
    """
    data = Artist.query.get(artist_id)
    artist_data = {}
    current_time = datetime.now()

    if data:
        past_results = (
            db.session.query(Musicshows)
            .filter(Musicshows.artist_id == artist_id)
            .filter(Musicshows.start_time < current_time)
            .all()
        )
        upcoming_results = (
            db.session.query(Musicshows)
            .filter(Musicshows.artist_id == artist_id)
            .filter(Musicshows.start_time > current_time)
            .all()
        )

        artist_data = Artist.details(data)
        artist_data["past_shows"] = list(map(Musicshows.venue_details, past_results))
        artist_data["upcoming_shows"] = list(
            map(Musicshows.venue_details, upcoming_results)
        )
        artist_data["past_shows_count"] = len(past_results)
        artist_data["upcoming_shows_count"] = len(upcoming_results)

    return render_template("pages/show_artist.html", artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route("/artists/<int:artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):
    """ populate form with fields from artist with artist_id and
    return the form for editing artist details.
    Arguments:
        artist_id {int} -- artist id
    Returns:
        form -- form fields
    """
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
    return render_template("forms/edit_artist.html", form=form, artist=artist)


@app.route("/artists/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    """take values from the form submitted and update
    existing artist record with artist_id
    Arguments:
        artist_id {int} -- artist id
    Returns:
        [int] -- artist id
    """

    form = ArtistForm(request.form)
    artist = Artist.query.get(artist_id)
    if artist:
        if form.is_submitted():
            print("Artist edit Form successfully submitted")
        if form.validate():
            print("Form validated")
            try:
                setattr(artist, "name", request.form["name"])
                setattr(artist, "genres", request.form.getlist("genres"))
                setattr(artist, "city", request.form["city"])
                setattr(artist, "state", request.form["state"])
                setattr(artist, "phone", request.form["phone"])
                setattr(artist, "website_link", request.form["website_link"])
                setattr(artist, "facebook_link", request.form["facebook_link"])
                setattr(artist, "image_link", request.form["image_link"])
                setattr(
                    artist, "seeking_description", request.form["seeking_description"]
                )
                setattr(artist, "seeking_venue", bool(request.form["seeking_venue"]))
                Artist.update(artist)
                flash("Edited Successfully")
            except SQLAlchemyError as e:
                flash("Edit failed!!")
                print(e)
                return render_template("errors/404.html")
    return redirect(url_for("show_artist", artist_id=artist_id))


@app.route("/venues/<int:venue_id>/edit", methods=["GET"])
def edit_venue(venue_id):
    """ populate form with fields from venue with venue_id and
    return the form for editing venue details.
    Arguments:
        venue_id {int} -- venue id
    Returns:
        form -- form fields
    """
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
    return render_template("forms/edit_venue.html", form=form, venue=venue)


@app.route("/venues/<int:venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
    """take values from the form submitted and update
    existing venue record with venue_id
    Arguments:
        venue_id {int} -- venue id
    Returns:
        [int] -- venue id
    """

    form = VenueForm(request.form)
    venue = Venue.query.get(venue_id)
    if venue:
        if form.validate():
            print("Form validated")
            try:
                setattr(venue, "name", request.form["name"])
                setattr(venue, "genres", request.form.getlist("genres"))
                setattr(venue, "city", request.form["city"])
                setattr(venue, "address", request.form["address"])
                setattr(venue, "state", request.form["state"])
                setattr(venue, "phone", request.form["phone"])
                setattr(venue, "facebook_link", request.form["facebook_link"])
                setattr(venue, "website_link", request.form["website_link"])
                setattr(venue, "image_link", request.form["image_link"])
                setattr(venue, "seeking_talent", bool(request.form["seeking_talent"]))
                setattr(
                    venue, "seeking_description", request.form["seeking_description"]
                )
                Venue.update(venue)
                flash("Edited Successfully")
            except SQLAlchemyError as e:
                flash("Edit failed!!")
                print(e)
                return render_template("errors/404.html")
    return redirect(url_for("show_venue", venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------


@app.route("/artists/create", methods=["GET"])
def create_artist_form():
    """gets artist form for creating new artist
    Returns:
        form -- artist form fields
    """
    form = ArtistForm()
    return render_template("forms/new_artist.html", form=form)


@app.route("/artists/create", methods=["POST"])
def create_artist_submission():
    """insert form data as a new artist record in db 
    """
    form = ArtistForm(request.form)
    if form.is_submitted():
        print("Form successfully submitted")

    if form.validate_on_submit():
        try:
            new_artist = Artist(
                name=request.form["name"],
                city=request.form["city"],
                state=request.form["state"],
                phone=request.form["phone"],
                facebook_link=request.form["facebook_link"],
                genres=request.form.getlist("genres"),
                image_link=request.form["image_link"],
                website_link=request.form["website_link"],
                seeking_venue=bool(request.form["seeking_venue"]),
                seeking_description=request.form["seeking_description"],
            )

            Artist.insert(new_artist)
            flash("Artist" + request.form["name"] + " was successfully listed!")

        except SQLAlchemyError as e:
            db.session.rollback()
            print(e)
            flash("OOPS!! Artist " + request.form["name"] + " was not listed!")
        finally:
            db.session.close()
    return render_template("pages/home.html")


#  Shows
#  ----------------------------------------------------------------


@app.route("/shows")
def shows():
    """display list of shows   
    Returns:
        dictionary -- show details
    """

    shows_data = {}
    data = db.session.query(Musicshows).all()

    shows_data = Musicshows.details(data)

    return render_template("pages/shows.html", shows=shows_data)


@app.route("/shows/create")
def create_shows():
    """renders form for registering a show.
    Returns:
        form -- show form fields
    """
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)


@app.route("/shows/create", methods=["POST"])
def create_show_submission():
    """called to create new show in db.
    upon submitting, insert form data as a new show
    """
    form = ShowForm(request.form)
    if form.validate_on_submit():
        try:
            new_show = Musicshows(
                artist_id=request.form["artist_id"],
                venue_id=request.form["venue_id"],
                start_time=request.form["start_time"],
            )
            Musicshows.insert(new_show)
        except SQLAlchemyError as e:
            db.session.rollback()
            print(e)
            flash("An error occurred. Show could not be listed.")
    return render_template("pages/home.html")


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == "__main__":
    app.run()

# Or specify port manually:
"""
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
"""

