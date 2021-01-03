from flask import Blueprint, request

access_token = Blueprint('access_token', __name__)


@access_token.route('/accessToken', methods=['GET'])
def get_access_token():
    from login_service.util.jwt_handler import JwtHandler
    data = request.headers
    return JwtHandler.get_access_token(data)
