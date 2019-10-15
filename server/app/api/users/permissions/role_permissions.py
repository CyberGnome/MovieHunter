import jwt
from flask import request, jsonify

from app import app
from functools import wraps
from app.models import Role


def roles_required(*roles):
    def wrapper(f):
        @wraps(f)    # Tells debuggers that is is a function wrapper
        def decorated(*args, **kwargs):
            user = args[0]
            user_roles = [x.name for x in Role.query.filter(Role.users.any(id=user.id))]
            for role in user_roles:
                print(role)
                print(roles)
                if role in roles:
                    return f(*args, **kwargs)

            return jsonify({'message': 'Permission denied!'}), 401
        return decorated
    return wrapper
