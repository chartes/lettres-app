from flask import jsonify, current_app, request, url_for
from flask_jwt_extended import create_access_token, set_access_cookies, \
    unset_jwt_cookies

from app import api_bp
from app.models import User
from flask_login import current_user


def refresh_token(user, resp=None):
    if not user.is_anonymous:
        access_token = create_access_token(identity=user.to_json(), fresh=True)
        auth_headers = {'login': True, 'user': url_for("api_bp.users_single_obj_endpoint", id=user.id)}
        if resp:
            resp.headers["login"] = auth_headers["login"]
            resp.headers["user"] = auth_headers["user"]
        else:
            resp = jsonify(auth_headers)
        set_access_cookies(resp, access_token)
        print("set cookies", user)
    else:
        auth_headers = {'logout': True, 'user': None}
        if resp:
            resp.headers["logout"] = auth_headers["logout"]
            resp.headers["user"] = auth_headers["user"]
        else:
            resp = jsonify(auth_headers)
        unset_jwt_cookies(resp)
        print("unset cookies")
    return resp, 200


@api_bp.route('/api/<api_version>/token/auth', methods=['POST'])
def create_token(api_version):
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = User.query.filter(User.username == username).first()
    from app.api.decorators import error_401

    if user is None:
        return error_401
    else:
        passwords_match = current_app.user_manager.verify_password(password, user.password)
        if not passwords_match:
            return error_401

    access_token = create_access_token(identity=user.to_json())
    ret = {'access_token': access_token}
    return jsonify(ret), 200


@api_bp.route('/api/<api_version>/token/refresh')
def refresh_token_route(api_version):
    return refresh_token(current_user)


# register manifest generation api url
from app.api.manifest.routes import *
