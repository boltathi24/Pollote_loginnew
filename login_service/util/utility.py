import os

import pyotp

from login_service.config import DevConfig, ProdConfig


class Util:
    config = None
    totp = None

    @classmethod
    def init_config(cls):
        # env = os.getenv('ENVIRONMENT').lower()
        env = 'dev'
        if env == 'dev':
            cls.config = DevConfig
        elif env == 'prod':
            cls.config = ProdConfig


    @classmethod
    def get_app_config(cls):
        return cls.config

    @classmethod
    def get_otp(cls):
        secret = pyotp.random_base32()
        cls.totp = pyotp.TOTP(secret, interval=3000)
        return cls.totp.now()
