from flask import request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims
from flask_login import current_user
from functools import wraps

from app.api.decorators import error_403_privileges, error_403_unhandled_error
from app.api.route_registrar import json_loads
from app.models import Lock


def manage_lock_addition():
    def wrap(view_function):
        @wraps(view_function)
        def wrapped_f(*args, **kwargs):

            try:
                r = json_loads(request.data)
                lock_user_id = r['data']['relationships']['user']['data'][0]['id']
            except Exception as e:
                return error_403_unhandled_error(e)

            verify_jwt_in_request()
            roles = get_jwt_claims()

            # contributor cannot add locks it does not own
            if 'admin' not in roles and current_user.id != lock_user_id:
                return error_403_privileges

            return view_function(*args, **kwargs)

        return wrapped_f

    return wrap


def manage_lock_update():
    def wrap(view_function):
        @wraps(view_function)
        def wrapped_f(*args, **kwargs):
            r = json_loads(request.data)
            print("TODO")
            return view_function(*args, **kwargs)
        return wrapped_f
    return wrap


def manage_lock_removal():
    def wrap(view_function):
        @wraps(view_function)
        def wrapped_f(*args, **kwargs):

            try:
                r = json_loads(request.data)
                lock_id = r['data'][0]['id']
                lock = Lock.query.filter(Lock.id == lock_id).first()
            except Exception as e:
                return error_403_unhandled_error(e)

            verify_jwt_in_request()
            roles = get_jwt_claims()

            # contributor cannot remove locks it does not own
            if 'admin' not in roles and current_user.id != lock.user_id:
                return error_403_privileges

            return view_function(*args, **kwargs)

        return wrapped_f

    return wrap
