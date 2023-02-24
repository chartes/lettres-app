import datetime
from flask import request
from app.api.user.facade import UserFacade
#from flask_jwt_extended import current_user
#verify_jwt_in_request, get_jwt_identity,
from functools import wraps

from app import db
from app.api.decorators import error_403_privileges, error_400_unhandled_error
from app.api.route_registrar import json_loads
from app.models import Lock, DATETIME_FORMAT, User


def manage_lock_addition():
    def wrap(view_function):
        @wraps(view_function)
        def wrapped_f(*args, **kwargs):
            #verify_jwt_in_request_optional()

            try:
                r = json_loads(request.data)
                lock_user_id = r['data']['relationships']['user']['data'][0]['id']
                current_user = User.query.filter(User.id == lock_user_id).first()

                old_locks = Lock.query.filter(
                    Lock.object_id == r['data']['attributes']['object-id'],
                    Lock.object_type == r['data']['attributes']['object-type']).order_by(Lock.event_date).all()
                active_lock = [l for l in old_locks if l.is_active]
                if len(active_lock) > 1:
                    raise Exception("Two locks are active at the same time on the same object: %s" % active_lock)

            except Exception as e:
                return error_400_unhandled_error(e)

            #roles = get_jwt_claims()
            #identity = get_jwt_identity()
            #current_user = User.query.filter(User.username == identity).first()
            if current_user is None:
                return error_403_privileges
            else:
                print(current_user.id, current_user.is_admin, lock_user_id, old_locks, active_lock)
                # contributor cannot add locks it does not own
                # contributor cannot add locks if an active lock already exists
                if not current_user.is_admin and (current_user.id != lock_user_id or len(active_lock) >= 1):
                    return error_403_privileges


            # if the doc is already locked, expire the previous locks on this object
            # TODO watch permissions first
            response = view_function(*args, **kwargs)
            if response.status.startswith("20"):
                new_lock = json_loads(response.data)
                previous_locks = Lock.query.filter(Lock.id != new_lock['data']['id'],
                                    Lock.object_id == new_lock['data']['attributes']['object-id'],
                                    Lock.object_type == new_lock['data']['attributes']['object-type']).all()

                for plock in previous_locks:
                    '''plock.expiration_date = datetime.datetime.strptime(
                        new_lock['data']['attributes']['event-date'],
                        DATETIME_FORMAT
                    )'''
                    db.session.delete(plock)
                db.session.commit()

            return response

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
            #verify_jwt_in_request(optional=True)
            r = json_loads(request.data)
            print(r)
            lock_user_id = r['relationships']['user']['data'][0]['id']
            current_user = User.query.filter(User.id == lock_user_id).first()
            lock_id = r['id']
            lock = Lock.query.filter(Lock.id == lock_id).first()
            print(current_user.id, current_user.is_admin, lock_user_id, lock_id)
            try:
                r = json_loads(request.data)
                lock_user_id = r['relationships']['user']['data'][0]['id']
                current_user = User.query.filter(User.id == lock_user_id).first()
                lock_id = r['id']
                lock = Lock.query.filter(Lock.id == lock_id).first()
                print(current_user.id, current_user.is_admin, lock_user_id)
            except Exception as e:
                return error_400_unhandled_error(e)

            #identity = get_jwt_identity()
            #current_user = User.query.filter(User.username == identity).first()
            if current_user is None:
                return error_403_privileges
            else:
                print(current_user.id, current_user.is_admin, lock_user_id, lock)
                # contributor cannot remove locks it does not own
                if not current_user.is_admin and current_user.id != lock.user_id:
                    return error_403_privileges

            # HOOK ici pour transformer le DELETE en UPDATE
            print("TODO: transformer le delete en update (déverrouillage")
            response = view_function(*args, **kwargs)
            if response.status.startswith("20"):
                db.session.delete(lock)
                db.session.commit()

            return response

        return wrapped_f

    return wrap
