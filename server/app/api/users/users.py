# -*- coding: utf-8 -*-
import datetime
from functools import wraps

import jwt
from flask import jsonify, request, make_response

from app import app, db
from app.api.users.permissions.user_permissions import roles_required, login_required
from app.models import User, Role


@app.route('/api/users/new/', methods=['POST'])
def registration_new_user():
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


@app.route('/api/users/login/', methods=['POST'])
def login_user():
    if not request.json:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=username).first()
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if not user.verify_password(password):
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    token = jwt.encode({'public_id': str(user.public_id),
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'])

    return jsonify(
        {'token': token.decode('UTF-8')})


@app.route('/api/users/', methods=['GET'])
@login_required
@roles_required(Role.RoleNames.ADMIN)
def get_all_users(current_user):
    users_list = [{'id': x.public_id, 'username': x.username} for x in User.query.all()]
    return jsonify({'users-list': users_list})


@app.route('/api/users/<public_id>/', methods=['GET'])
@login_required
@roles_required(Role.RoleNames.ADMIN)
def get_user_info_by_id(current_user, public_id):
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
@login_required
@roles_required(Role.RoleNames.ADMIN)
def delete_user_by_id(current_user, public_id):
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
