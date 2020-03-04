from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    SelectMultipleField,
    DateTimeField,
    BooleanField,
    ValidationError,
)
from wtforms.validators import DataRequired, AnyOf, URL
import re

state_choices = [
    ("AL", "AL"),
    ("AK", "AK"),
    ("AZ", "AZ"),
    ("AR", "AR"),
    ("CA", "CA"),
    ("CO", "CO"),
    ("CT", "CT"),
    ("DE", "DE"),
    ("DC", "DC"),
    ("FL", "FL"),
    ("GA", "GA"),
    ("HI", "HI"),
    ("ID", "ID"),
    ("IL", "IL"),
    ("IN", "IN"),
    ("IA", "IA"),
    ("KS", "KS"),
    ("KY", "KY"),
    ("LA", "LA"),
    ("ME", "ME"),
    ("MT", "MT"),
    ("NE", "NE"),
    ("NV", "NV"),
    ("NH", "NH"),
    ("NJ", "NJ"),
    ("NM", "NM"),
    ("NY", "NY"),
    ("NC", "NC"),
    ("ND", "ND"),
    ("OH", "OH"),
    ("OK", "OK"),
    ("OR", "OR"),
    ("MD", "MD"),
    ("MA", "MA"),
    ("MI", "MI"),
    ("MN", "MN"),
    ("MS", "MS"),
    ("MO", "MO"),
    ("PA", "PA"),
    ("RI", "RI"),
    ("SC", "SC"),
    ("SD", "SD"),
    ("TN", "TN"),
    ("TX", "TX"),
    ("UT", "UT"),
    ("VT", "VT"),
    ("VA", "VA"),
    ("WA", "WA"),
    ("WV", "WV"),
    ("WI", "WI"),
    ("WY", "WY"),
]

genre_choices = [
    ("Alternative", "Alternative"),
    ("Blues", "Blues"),
    ("Classical", "Classical"),
    ("Country", "Country"),
    ("Electronic", "Electronic"),
    ("Folk", "Folk"),
    ("Funk", "Funk"),
    ("Hip-Hop", "Hip-Hop"),
    ("Heavy Metal", "Heavy Metal"),
    ("Instrumental", "Instrumental"),
    ("Jazz", "Jazz"),
    ("Musical Theatre", "Musical Theatre"),
    ("Pop", "Pop"),
    ("Punk", "Punk"),
    ("R&B", "R&B"),
    ("Reggae", "Reggae"),
    ("Rock n Roll", "Rock n Roll"),
    ("Soul", "Soul"),
    ("Other", "Other"),
]


class ShowForm(FlaskForm):
    artist_id = StringField("artist_id", validators=[DataRequired()])
    venue_id = StringField("venue_id", validators=[DataRequired()])
    start_time = DateTimeField(
        "start_time", validators=[DataRequired()], default=datetime.today()
    )


def validate_phone(form, field):
    if not re.search(r"^[0-9]{10}$", field.data):
        raise ValidationError("Invalid Phone number")


def validate_state(form, field):
    all_states = [state[1] for state in state_choices]
    value = field.data
    if value not in all_states:
        raise ValidationError("Invalid state")


def validate_genres(form, field):
    all_genres = [choice[1] for choice in genre_choices]
    for value in field.data:
        if value not in all_genres:
            raise ValidationError("Invalid genre")


def length(form, field):
    if len(field.data) > 100 or len(field.data) < 10:
        raise ValidationError("Field description must be between 10 to 100")


class VenueForm(FlaskForm):

    name = StringField("name", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    state = SelectField(
        "state", validators=[DataRequired(), validate_state], choices=state_choices
    )
    address = StringField("address", validators=[DataRequired()])
    phone = StringField("phone", validators=[DataRequired(), validate_phone])
    image_link = StringField("image_link", validators=[DataRequired(), URL()])
    genres = SelectMultipleField(
        "genres",
        validators=[DataRequired(), validate_genres],
        choices=genre_choices,
    )
    facebook_link = StringField("facebook_link", validators=[DataRequired(), URL()])

    website_link = StringField("website_link", validators=[DataRequired(), URL()])
    seeking_talent = BooleanField("seeking_talent", validators=[DataRequired()])
    seeking_description = StringField(
        "seeking_description", validators=[DataRequired(), length]
    )


class ArtistForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    state = SelectField(
        "state", validators=[DataRequired(), validate_state], choices=state_choices
    )
    phone = StringField(
        "phone",
        validators=[DataRequired(), validate_phone],
    )
    image_link = StringField("image_link", validators=[DataRequired(), URL()])
    genres = SelectMultipleField(
        "genres",
        validators=[DataRequired(), validate_genres],
        choices=genre_choices,
    )
    facebook_link = StringField(
        "facebook_link",
        validators=[DataRequired(), URL()],
    )
    website_link = StringField("website_link", validators=[DataRequired(), URL()])
    seeking_venue = BooleanField("seeking_venue", validators=[DataRequired()])
    seeking_description = StringField(
        "seeking_description", validators=[DataRequired(), length]
    )

