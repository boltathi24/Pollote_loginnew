import json

from flask import Blueprint, jsonify, request
from passlib.hash import bcrypt

from login_service.models.user import User

sign_in = Blueprint('signIn', __name__)


@sign_in.route('/signIn', methods=['POST'])
def login():
    from login_service.util.jwt_handler import JwtHandler
    data = json.loads(request.data)
    tokens = JwtHandler.get_tokens(data["username"])[0].json
    result_set = User.objects(username=data['username'])
    if not result_set:
        return jsonify({'success': False, 'message': 'Username does not exist'}), 400
    if bcrypt.verify(data['password'], result_set.only('password').first().password):
        User.objects(username=data['username']).update(refresh_token=tokens['refresh_token'])
        tokens['message'] = 'Login successful'
        return jsonify(tokens), 200
    else:
        return jsonify({'success': False, 'message': 'Incorrect Password'}), 400


@sign_in.route('/signOut', methods=['GET'])
def logout():
    from login_service.util.jwt_handler import JwtHandler
    headers = request.headers
    args = request.args
    is_valid_access = JwtHandler.validate_access_token(headers)
    if is_valid_access[0].json['success']:
        User.objects(username=args['username']).update(refresh_token='')
        return jsonify({"success": True, "message": "Sign out successful"}), 200
    else:
        return is_valid_access
