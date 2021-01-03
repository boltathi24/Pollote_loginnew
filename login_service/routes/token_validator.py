from flask import Blueprint, request

token_validator = Blueprint('api', __name__)


@token_validator.route('/tokenValidator', methods=['GET'])
def access_token():
    from login_service.util.jwt_handler import JwtHandler
    data = request.headers
    return JwtHandler.validate_access_token(data)
