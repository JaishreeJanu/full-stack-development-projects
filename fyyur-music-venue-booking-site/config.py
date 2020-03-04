import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to a local postgresql database server:  DATABASE URL -->
SQLALCHEMY_DATABASE_URI = "postgres://{}:{}@{}/{}".format('jaishree','password','localhost:5432','fyyur')
SQLALCHEMY_TRACK_MODIFICATIONS = False