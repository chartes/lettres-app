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


# register manifest generation api url
from app.api.manifest.routes import *
