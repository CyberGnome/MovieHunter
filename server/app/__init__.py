from flask import Flask

from settings import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.api.users.users import *
from app.api.movies.movies import *
from app.api.genre.genre import *
from app import models
