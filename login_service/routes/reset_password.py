import json

from flask import Blueprint, jsonify, request
from passlib.hash import bcrypt

from login_service.util.mail import Mail
from login_service.models.user import User
from login_service.util.utility import Util

reset_pwd = Blueprint('reset_password', __name__)


@reset_pwd.route('/sendOtp', methods=['GET'])
def send_otp():
    from login_service.util.jwt_handler import JwtHandler
    headers = request.headers
    args = request.args
    is_valid_access = JwtHandler.validate_access_token(headers)
    if is_valid_access[0].json['success']:
        user = User.objects(username=args['username']).only('email').first()
        text = 'Dear ' + args['username'] + """,
        Your OTP for password reset is """ + Util.get_otp()
        response = Mail.send_mail(user.email, 'Pollote_Login_Service - Reset Password', text)
        if response[0].json['success']:
            return jsonify({'success': True, 'message': 'OTP sent to user'}), 200
        else:
            return response
    else:
        return is_valid_access


@reset_pwd.route('/checkOtp', methods=['GET'])
def check_otp():
    from login_service.util.jwt_handler import JwtHandler
    headers = request.headers
    args = request.args
    is_valid_access = JwtHandler.validate_access_token(headers)
    if is_valid_access[0].json['success']:
        if Util.totp.verify(args['OTP']):
            return jsonify({'success': True, 'message': 'OTP is valid'}), 200
        else:
            return jsonify({'success': False, 'message': 'Invalid OTP or OTP has been expired'}), 400
    else:
        return is_valid_access


@reset_pwd.route('/resetPassword', methods=['POST'])
def reset_password():
    from login_service.util.jwt_handler import JwtHandler
    headers = request.headers
    data = json.loads(request.data)
    is_valid_access = JwtHandler.validate_access_token(headers)
    if is_valid_access[0].json['success']:
        try:
            hashed_password = bcrypt.hash(data['password'])
            User.objects(username=data['username']).update(password=hashed_password)
            return jsonify({'success': True, "message": "Password changed successfully"}), 200
        except Exception as e:
            return jsonify({'success': False, 'message': 'Reset Password failed!', 'Exception': str(e)}), 400
    else:
        return is_valid_access
