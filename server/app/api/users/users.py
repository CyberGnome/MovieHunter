# -*- coding: utf-8 -*-
from flask import jsonify, request, abort, url_for

from app import app, db
from app.models import User, Role


@app.route('/api/users/new/', methods=['POST'])
def new_user():
    if not request.json:
        return jsonify(
            {'error': "Bad Request"}), 400

    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        return jsonify(
            {'error': "Bad Request"}), 400

    if User.query.filter_by(username=username).first() is not None:
        return jsonify(
            {'error': "User with this login already exists!"}), 400

    user = User(username=username)
    user.hash_password(password)

    role = Role.query.filter_by(name=Role.RoleNames.USER).first()
    if role is None:
        return jsonify(
            {'error': "There is no user role in the database!"}), 500

    user.role.append(role)
    db.session.add(user)
    db.session.commit()

    return jsonify(
        {'username': user.username}), 201


@app.route('/api/users/', methods=['GET'])
def users_list():
    users_list = [{'id': x.id, 'username': x.username} for x in User.query.all()]
    return jsonify({'articles-list': users_list})
