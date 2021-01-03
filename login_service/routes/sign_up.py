import json

from flask import Blueprint, jsonify, request
from passlib.hash import bcrypt

from login_service.models.user import User

sign_up = Blueprint('sign_up', __name__)


@sign_up.route('/signup', methods=['POST'])
def register():
    from login_service.util.jwt_handler import JwtHandler
    data = json.loads(request.data)
    tokens = JwtHandler.get_tokens(data["username"])[0].json
    try:
        hashed_password = bcrypt.hash(data['password'])
        User(username=data['username'], email=data['email'], password=hashed_password,
             refresh_token=tokens['refresh_token']).save()
        tokens['message'] = 'Registered successfully'
        return jsonify(tokens), 200
    except Exception as e:
        return jsonify({'success': False, 'message': 'Registration failed!', 'Exception': str(e)}), 400
