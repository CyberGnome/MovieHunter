# -*- coding: utf-8 -*-
import datetime
from functools import wraps

import jwt
from flask import jsonify, request, abort, g, make_response
from werkzeug.security import check_password_hash

from app import app, db
from app.models import User, Role


@app.route('/api/users/new/', methods=['POST'])
def new_user():
    if not request.json:
        return jsonify(
            {'message': "Bad Request"}), 400

    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        return jsonify(
            {'message': "Bad Request"}), 400

    if User.query.filter_by(username=username).first() is not None:
        return jsonify(
            {'message': "User with this login already exists!"}), 400

    user = User(username=username)
    user.hash_password(password)

    role = Role.query.filter_by(name=Role.RoleNames.USER).first()
    if role is None:
        return jsonify(
            {'message': "There is no user role in the database!"}), 500

    user.role.append(role)
    db.session.add(user)
    db.session.commit()

    return jsonify(
        {'username': user.username,
         'message': "New user created"}), 201


@app.route('/api/users/<public_id>/', methods=['GET'])
def get_user_by_id(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify(
            {'message': "User not found!"})

    return jsonify(
            {'username': user.username,
             'created_date': user.created,
             'public_id': user.public_id,
             'user_roles': [{'id': x.id, 'role-name': str(x.name)} for x in Role.query.filter(Role.users.any(id=user.id))]})


@app.route('/api/users/<public_id>/', methods=['DELETE'])
def delete_user_by_id(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify(
            {'message': "User not found!"})

    username = user.username
    db.session.delete(user)
    db.session.commit()

    return jsonify(
            {'message': "User was deleted!",
             "username": username})


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/api/users/', methods=['GET'])
@token_required
def get_all_users(current_user):
    users_list = [{'id': x.public_id, 'username': x.username} for x in User.query.all()]
    return jsonify({'users-list': users_list})


@app.route('/api/users/login/')
def login_user():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=auth.username).first()
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if not user.verify_password(auth.password):
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    token = jwt.encode({'public_id': str(user.public_id),
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'])

    return jsonify(
        {'token': token.decode('UTF-8')})
