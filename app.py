from flask import Flask
from mongoengine import connect

from login_service.routes import access_token
from login_service.routes import reset_password
from login_service.routes import sign_in
from login_service.routes import sign_up
from login_service.routes import token_validator
from login_service.util.utility import Util

application=Flask(__name__)

# def create_app():
#     app = Flask(__name__)
#     app.register_blueprint(sign_up, url_prefix='/api')
#     app.register_blueprint(sign_in, url_prefix='/api')
#     app.register_blueprint(token_validator, url_prefix='/api')
#     app.register_blueprint(reset_pwd, url_prefix='/api')
#     app.register_blueprint(access_token, url_prefix='/api')
#     return app

@application.route("/api/auth/signup",methods=['POST'])
def signup():
    return sign_up.register()

@application.route("/api/auth/signIn",methods=['POST'])
def signin():
    return sign_in.login()

@application.route("/api/auth/signOut",methods=['GET'])
def signout():
    return sign_in.logout()

@application.route("/api/auth/tokenValidator",methods=['GET'])
def validatetoken():
    return token_validator.access_token()

@application.route("/api/auth/access_token",methods=['GET'])
def getAccesToken():
    return access_token.get_access_token()

@application.route("/api/auth/resetPassword",methods=['POST'])
def resetPwd():
    return reset_password.reset_password()

@application.route("/api/auth/checkOtp",methods=['GET'])
def checkOtp():
    return reset_password.check_otp()

@application.route("/api/auth/sendOtp",methods=['GET'])
def sendOtp():
    return reset_password.send_otp()






if __name__ == '__main__':
    Util.init_config()
    conn = connect(   db='Pollote',
    username='boltathi24',
    password='ZohoTest@24',
    host='mongodb+srv://cluster0.xckok.mongodb.net').Util.config.DATABASE
    application.run(host=Util.config.APP_HOST, port=Util.config.APP_PORT)
