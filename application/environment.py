import os
from dotenv import load_dotenv

#basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()

class Environment(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'LaVieEinRoseIz*one')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Production(Environment):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql://postgres:password@localhost:5432/opdb')

class Staging(Environment):
    DEVELOPMENT = True
    DEBUG = True

class Development(Environment):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql://postgres:password@localhost:5432/opdevdb')

class Testing(Environment):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql://postgres:password@localhost:5432/opuntdb')
