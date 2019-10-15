import jwt
from flask import jsonify, request

from functools import wraps

from app import app
from app.models import Role, User


def roles_required(*roles):
    def wrapper(f):
        @wraps(f)    # Tells debuggers that is is a function wrapper
        def decorated(*args, **kwargs):
            user = args[0]
            user_roles = [x.name for x in Role.query.filter(Role.users.any(id=user.id))]
            for role in user_roles:
                if role in roles:
                    return f(*args, **kwargs)

            return jsonify({'message': 'Permission denied!'}), 401
        return decorated
    return wrapper


def login_required(f):
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
