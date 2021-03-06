from flask import session, current_app
from flask_jwt_extended import get_jwt_identity, get_jwt_claims, jwt_required, verify_jwt_in_request
from functools import wraps
from app import JSONAPIResponseFactory


error_401 = JSONAPIResponseFactory.make_errors_response(
    {
        "status": 401,
        "title": "Unauthorized"
    },
    status=401
)

error_403_privileges = JSONAPIResponseFactory.make_errors_response(
    {
        "status": 403,
        "title": "Insufficient privileges"
    },
    status=403
)

def error_400_unhandled_error(e):
    return JSONAPIResponseFactory.make_errors_response(
        {
            "status": 400,
            "title": "Unhandled error. Check your data",
            "details": str(e)
        },
        status=400
)


def api_require_roles(*required_roles):
    def wrap(view_function):
        @wraps(view_function)
        def wrapped_f(*args, **kwargs):
            verify_jwt_in_request()
            ret = {
                'current_identity': get_jwt_identity(),  # username
                'current_roles': get_jwt_claims()  # roles
            }
            print("You are %s." % ret, "You need to be", required_roles)
            for required_role in required_roles:
                if required_role not in ret["current_roles"]:
                    print("Sorry, you are not '" + required_role + "'")
                    return error_401
            res = view_function(*args, **kwargs)
            return res
        return wrapped_f
    return wrap
