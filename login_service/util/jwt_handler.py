__author__ = "Kapil"
import datetime

import jwt
from flask import jsonify
from login_service.util.utility import Util

from login_service.models.user import User


class JwtHandler:
    config = Util.config

    @classmethod
    def get_tokens(cls, username):
        refresh_token_json = cls.generate_refresh_token(username)
        if refresh_token_json[0].json['success']:
            refresh_token = refresh_token_json[0].json['refresh_token']
            access_token_json = cls.generate_access_token(refresh_token)
            if access_token_json[0].json['success']:
                access_token = access_token_json[0].json['access_token']
                return jsonify({'success': True, 'refresh_token': refresh_token, 'access_token': access_token,
                                'access_token_expiration_min': cls.config.ACCESS_EXP_MIN}), 200
            else:
                return access_token_json
        else:
            return refresh_token_json

    @classmethod
    def get_access_token(cls, header):
        if 'refresh_token' in header:
            refresh_token = header.get('refresh_token')
            username_payload = cls.get_handler_name_by_decoding_refresh_token(refresh_token)
            if username_payload[0].json['success']:
                refresh_token_from_db = User.objects(username=username_payload[0].json['username'])\
                    .only('refresh_token').first().refresh_token
                if refresh_token_from_db == refresh_token:
                    return cls.generate_access_token(header['refresh_token'])
                else:
                    return jsonify({"success": False, "message": "Invalid refresh token"}), 400
            else:
                return username_payload
        else:
            return jsonify({"success": False, "message": "Provide refresh token"}), 400

    @classmethod
    def validate_access_token(cls, header):
        if 'access_token' in header:
            try:
                access_token = header["access_token"]
                refresh_token_payload = cls.get_refresh_token_by_decoding_access_token(access_token)
                if refresh_token_payload[0].json['success']:
                    refresh_token = refresh_token_payload[0].json['refresh_token']
                    username_payload = cls.get_handler_name_by_decoding_refresh_token(refresh_token)
                    if username_payload[0].json['success']:
                        refresh_token_from_db = User.objects(username=username_payload[0].json['username'])\
                            .only('refresh_token').first().refresh_token
                        if refresh_token_from_db == refresh_token:
                            return jsonify({"success": True, "message": "Valid access token"}), 200
                        elif refresh_token_from_db == '':
                            return jsonify({"success": False, "message": "User session expired. Try login again."}), 400
                        else:
                            return jsonify({"success": False, "message": "Invalid access token"}), 400
                    else:
                        return username_payload
                else:
                    return refresh_token_payload
            except Exception as e:
                return jsonify({"success": False, "message": str(e)}), 400
        else:
            return jsonify({"success": False, "message": "Please Provide JWT Token"}), 400

    @classmethod
    def get_handler_name_by_decoding_refresh_token(cls, refresh_token):
        try:
            payload = cls.decode_token(refresh_token, cls.config.REFRESH_SEC_KEY)
            return jsonify({"success": True, "message": "Refresh token decoded",
                            "username": payload['username']}), 200
        except jwt.ExpiredSignatureError:
            return jsonify({"success": False, "message": "Access token has been expired"}), 400
        except jwt.InvalidTokenError:
            return jsonify({"success": False, "message": "Invalid access Token"}), 400

    @classmethod
    def get_refresh_token_by_decoding_access_token(cls, access_token):
        try:
            payload = cls.decode_token(access_token, cls.config.ACCESS_SEC_KEY)
            return jsonify({"success": True, "message": "Access token decoded",
                            "refresh_token": payload['refresh_token']}), 200
        except jwt.ExpiredSignatureError:
            return jsonify({"success": False, "message": "Access token has been expired"}), 400
        except jwt.InvalidTokenError:
            return jsonify({"success": False, "message": "Invalid access Token"}), 400

    @classmethod
    def generate_access_token(cls, refresh_token):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=cls.config.ACCESS_EXP_MIN),
                'refresh_token': refresh_token
            }
            access_token = cls.encode_token(payload, cls.config.ACCESS_SEC_KEY).decode('utf-8')
            return jsonify({"success": True, "message": "Access token", "access_token": access_token}), 200
        except Exception as e:
            return jsonify({"success": False, "message": "exception while generating access token",
                            "exception": str(e)}), 400

    @classmethod
    def generate_refresh_token(cls, username):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=cls.config.REFRESH_EXP_MIN),
                'username': username
            }
            refresh_token = cls.encode_token(payload, cls.config.REFRESH_SEC_KEY).decode('utf-8')
            return jsonify({"success": True, "message": "Refresh token", "refresh_token": refresh_token,
                            "username": username}), 200
        except Exception as e:
            return jsonify({"success": False, "message": "exception while generating refresh token",
                            "exception": str(e)}), 400

    @classmethod
    def encode_token(cls, payload, sec_key):
        return jwt.encode(payload, sec_key, algorithm='HS256')

    @classmethod
    def decode_token(cls, token, sec_key):
        return jwt.decode(token, sec_key)
