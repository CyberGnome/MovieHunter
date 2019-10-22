# -*- coding: utf-8 -*-
import enum
import string
import uuid
from datetime import datetime
from random import random

from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.dialects.postgresql import UUID

from app import db, app


def salt(length=128):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


MovieGenre = db.Table(
    'movie_genre',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True)
)

MovieProducer = db.Table(
    'movie_producer',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('producer_id', db.Integer, db.ForeignKey('producer.id'), primary_key=True)
)

MovieCountry = db.Table(
    'movie_country',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('country_id', db.Integer, db.ForeignKey('country.id'), primary_key=True)
)

# M2M сделано не случайно. Планируется, что в будущем у пользователя может быть несколько ролей
UserRole = db.Table(
    'user_role',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)


class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column('title', db.UnicodeText, nullable=False)
    year = db.Column('year', db.SmallInteger, nullable=False)
    annotation = db.Column('annotation', db.UnicodeText, nullable=True)
    adult = db.Column('adult', db.Boolean, default=False)
    age_restrictions = db.Column('age_restrictions', db.SmallInteger, nullable=True)

    logo_id = db.Column(db.Integer, db.ForeignKey('logo.id'), nullable=True)
    logo = db.relationship('Logo', backref='movies')

    rating_id = db.Column(db.Integer, db.ForeignKey('rating.id'), nullable=False)
    rating = db.relationship('Rating', backref='movies')

    genres = db.relationship('Genre', secondary=MovieGenre, lazy='subquery',
                             backref=db.backref('movies', lazy=True))
    producer = db.relationship('Producer', secondary=MovieProducer, lazy='subquery',
                               backref=db.backref('movies', lazy=True))
    country = db.relationship('Country', secondary=MovieCountry, lazy='subquery',
                              backref=db.backref('movies', lazy=True))


class Producer(db.Model):
    __tablename__ = 'producer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.UnicodeText, nullable=False)


class Genre(db.Model):
    __tablename__ = 'genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.UnicodeText, nullable=False, unique=True)


class Url(db.Model):
    __tablename__ = 'url'

    id = db.Column(db.Integer, primary_key=True)
    url_path = db.Column('url', db.UnicodeText, nullable=False)
    description = db.Column('description', db.UnicodeText, nullable=True)
    is_valid = db.Column('is_valid', db.Boolean, default=True)
    is_torrent = db.Column('is_torrent', db.Boolean, default=False)

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    movie = db.relationship('Movie', backref='movies')


class Logo(db.Model):
    __tablename__ = 'logo'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('path', db.UnicodeText, nullable=False)


class Country(db.Model):
    __tablename__ = 'country'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.UnicodeText, nullable=False)


class Rating(db.Model):
    __tablename__ = 'rating'

    id = db.Column(db.Integer, primary_key=True)
    web_site = db.Column('web_site', db.UnicodeText, nullable=False)
    rating_value = db.Column('value', db.Float, nullable=False)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    username = db.Column(db.String(32), index=True)
    password = db.Column(db.String(128), nullable=False)
    password_salt = db.Column(db.String(128), default=salt)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    role = db.relationship('Role', secondary=UserRole, lazy='subquery',
                           backref=db.backref('users', lazy=True))

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)


class Role(db.Model):
    __tablename__ = 'role'

    class RoleNames(enum.Enum):
        ADMIN = "Admin"
        USER = "User"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(RoleNames))
