from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField,ValidationError
from wtforms.validators import DataRequired, AnyOf, URL
from flask import flash
import re

state_choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]

genre_choices=[
    ('Alternative', 'Alternative'),
    ('Blues', 'Blues'),
    ('Classical', 'Classical'),
    ('Country', 'Country'),
    ('Electronic', 'Electronic'),
    ('Folk', 'Folk'),
    ('Funk', 'Funk'),
    ('Hip-Hop', 'Hip-Hop'),
    ('Heavy Metal', 'Heavy Metal'),
    ('Instrumental', 'Instrumental'),
    ('Jazz', 'Jazz'),
    ('Musical Theatre', 'Musical Theatre'),
    ('Pop', 'Pop'),
    ('Punk', 'Punk'),
    ('R&B', 'R&B'),
    ('Reggae', 'Reggae'),
    ('Rock n Roll', 'Rock n Roll'),
    ('Soul', 'Soul'),
    ('Other', 'Other'),
        ]


class ShowForm(FlaskForm):
    artist_id = StringField(
        'artist_id', validators=[DataRequired()]
    )
    venue_id = StringField(
        'venue_id', validators=[DataRequired()]
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

def validate_phone(form,field):
        if not re.search(r"^[0-9]{10}$", field.data):
            flash('please enter correct phone!!')
            raise ValidationError('Invalid Phone number')

def length(form,field):
    if len(field.data)>100 or len(field.data)<10:
        flash('Field description must be between 10 to 100!!')
        raise ValidationError('Field description must be between 10 to 100')


class VenueForm(FlaskForm):

    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired(),AnyOf(state_choices,message='Please select valid choices only')],
        choices=state_choices
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone', validators=[DataRequired(),validate_phone]
    )
    image_link = StringField(
        'image_link',validators=[DataRequired(),URL()]
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction ****
        'genres', validators=[DataRequired(),AnyOf(genre_choices,message='Please select valid choices only')],
        choices=genre_choices
    )
    facebook_link = StringField(
        'facebook_link', validators=[DataRequired(), URL()]
    )
    
    website_link = StringField(
        'website_link',validators=[DataRequired(), URL()]
    )
    seeking_talent = BooleanField(
        'seeking_talent',validators=[DataRequired()]
    )
    seeking_description = StringField(
        'seeking_description', validators=[DataRequired(), length]
    )

class ArtistForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired(),AnyOf(state_choices,message='Please select valid choices only')],
        choices=state_choices
    )
    phone = StringField(
        # TODO implement validation logic for state ****
        'phone', validators=[DataRequired(),validate_phone]
    )
    image_link = StringField(
        'image_link', validators=[DataRequired(),URL()]
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction ****
        'genres', validators=[DataRequired(),AnyOf(state_choices,message='Please select valid choices only')],
        choices=genre_choices
    )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[DataRequired(), URL()]
    )
    website_link = StringField(
        'website_link',validators=[DataRequired(), URL()]
    )
    seeking_venue = BooleanField(
        'seeking_venue', validators=[DataRequired()]
    )
    seeking_description = StringField(
        'seeking_description', validators=[DataRequired(), length]
    )

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM ****
