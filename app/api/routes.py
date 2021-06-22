from datetime import timedelta, datetime

import jwt
from flask import jsonify

from app import api_bp, db
from app.models import User


@api_bp.route('/api/<api_version>/register', methods=('POST',))
def register(api_version):
    data = request.get_json()
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_json()), 201


@api_bp.route('/api/<api_version>/login', methods=('POST',))
def login(api_version):
    data = request.get_json()
    user = User.authenticate(**data)

    if not user:
        return jsonify({'message': 'Invalid credentials', 'authenticated': False}), 401

    token = jwt.encode({
        'sub': user.email,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=60*24)},
        current_app.config['SECRET_KEY'])
    return jsonify({'token': token.decode('UTF-8'), 'user_data': user.to_json()})


@api_bp.route('/api/<api_version>/current-user', methods=('GET',))
def current_user(api_version):
    auth_headers = request.headers.get('Authorization', '').split()

    token = auth_headers[1]

    print("token", auth_headers, token)
    data = jwt.decode(token, current_app.config['SECRET_KEY'])
    user = User.query.filter_by(email=data['sub']).first()

    if not user:
        return jsonify({'message': 'Invalid credentials', 'authenticated': False}), 401

    return jsonify({'token': token, 'user_data': user.to_json()})

#def refresh_token(user, resp=None):
#    if not user.is_anonymous:
#        expires = timedelta(days=10)
#        access_token = create_access_token(identity=user.to_json(), fresh=True, expires_delta=expires)
#        auth_headers = {'login': True, 'user': url_for("api_bp.users_single_obj_endpoint", id=user.id)}
#        if resp:
#            resp.headers["login"] = auth_headers["login"]
#            resp.headers["user"] = auth_headers["user"]
#        else:
#            resp = jsonify(auth_headers)
#        set_access_cookies(resp, access_token)
#        print("token refreshed")
#    else:
#        auth_headers = {'logout': True, 'user': None}
#        if resp:
#            resp.headers["logout"] = auth_headers["logout"]
#            resp.headers["user"] = auth_headers["user"]
#        else:
#            resp = jsonify(auth_headers)
#        unset_jwt_cookies(resp)
#        print("token cleared")
#    return resp, 200
#
#
#@api_bp.route('/api/<api_version>/token/auth', methods=['POST'])
#def create_token(api_version):
#    username = request.json.get('username', None)
#    password = request.json.get('password', None)
#
#    user = User.query.filter(User.username == username).first()
#    from app.api.decorators import error_401
#
#    if user is None:
#        return error_401
#    else:
#        passwords_match = current_app.user_manager.verify_password(password, user.password)
#        if not passwords_match:
#            return error_401
#
#    expires = timedelta(days=10)
#    access_token = create_access_token(identity=user.to_json(), expires_delta=expires)
#    ret = {'access_token': access_token}
#    return jsonify(ret), 200
#
#
#@api_bp.route('/api/<api_version>/token/refresh')
#def refresh_token_route(api_version):
#    return refresh_token(current_user)
#
#def create_tokens(user):
#    u = user.to_json()
#    access_token = create_access_token(identity=u, fresh=True)
#    refresh_token = create_refresh_token(u)
#    data = {
#        'username': user.username,
#        'firstname': user.first_name,
#        'lastname': user.last_name,
#        'id': user.id,
#        'email': user.email,
#        'roles': [r.name for r in user.roles]
#    }
#    return data, access_token, refresh_token,
#

#@api_bp.route('/api/<api_version>/login', methods=['POST'])
#def login(api_version):
#    json = request.get_json(force=True)
#    username = json.get('email', None)
#    password = json.get('password', None)
#    user = User.query.filter(or_(User.username == username, User.email == username)).first()
#    from app.api.decorators import error_401
#
#    if user is None:
#        return error_401
#
#    passwords_match = check_password_hash(user.password, password)
#    if not passwords_match:
#        return error_401
#
#    data, access_token, refresh_token = create_tokens(user)
#
#    resp = jsonify(data)
#
#    set_access_cookies(resp, access_token)
#    set_refresh_cookies(resp, refresh_token)
#
#    print("login:", resp.headers)
#
#    return resp, 200


#@api_bp.route('/api/<api_version>/refresh', methods=['POST'])
#@jwt_refresh_token_required
#def refresh(api_version):
#    user = get_jwt_identity()
#    user = User.query.filter(User.username == user).first()
#    if user is None:
#        from app.api.decorators import error_403_privileges
#        return error_403_privileges
#
#    data, access_token, refresh_token = create_tokens(user)
#
#    resp = jsonify(data)
#
#    set_access_cookies(resp, access_token)
#    set_refresh_cookies(resp, refresh_token)
#    print("token refreshed")
#
#    return resp, 200
#

# register manifest generation api url
from app.api.manifest.routes import *
