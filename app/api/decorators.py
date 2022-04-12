import jwt
from flask import session, current_app, request, jsonify
from functools import wraps
from app import JSONAPIResponseFactory
from app.models import User

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
    def token_required_wrapper(view_function):
        @wraps(view_function)
        def _verify(*args, **kwargs):
            auth_headers = request.headers.get('Authorization', '').split()

            invalid_msg = {
                'message': 'Invalid token. Registeration and / or authentication required',
                'authenticated': False
            }
            expired_msg = {
                'message': 'Expired token. Reauthentication required.',
                'authenticated': False
            }

            if len(auth_headers) != 2:
                return jsonify(invalid_msg), 401

            try:
                token = auth_headers[1]
                data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
                user = User.query.filter_by(email=data['sub']).first()
                if not user:
                    raise RuntimeError('User not found')

                for required_role in required_roles:
                    if required_role not in [r.name for r in user.roles]:
                        print("Sorry, you are not '" + required_role + "'")
                        return error_401

                return view_function(*args, **kwargs)

            except jwt.ExpiredSignatureError:
                return jsonify(expired_msg), 401  # 401 is Unauthorized HTTP status code

            except (jwt.InvalidTokenError, Exception) as e:
                print(e)
                return jsonify(invalid_msg), 401

        return _verify

    return token_required_wrapper
