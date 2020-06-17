from flask_sqlalchemy import SQLAlchemy
from .environment import Development, Production, Staging, Testing

environments = dict(
    development=Development,
    production=Production,
    staging=Staging,
    testing=Testing
)

database = SQLAlchemy()