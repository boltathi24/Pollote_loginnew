class DevConfig:
    CONFIG_NAME = "dev"
    DEBUG = True
    DATABASE = 'Pollote'
    DB_HOST = 'localhost'
    DB_PORT = 27017
    DB_USERNAME = ''
    DB_PASSWORD = ''
    APP_HOST = '127.0.0.1'
    APP_PORT = '8080'
    REFRESH_SEC_KEY = '21345'
    ACCESS_SEC_KEY = '34213'
    REFRESH_EXP_MIN = 3000
    ACCESS_EXP_MIN = 200


class ProdConfig:
    CONFIG_NAME = "prod"
    DEBUG = False
    DATABASE = 'Pollote'
    DB_HOST = 'localhost'
    DB_PORT = 27017
    DB_USERNAME = ''
    DB_PASSWORD = ''
    APP_HOST = '127.0.0.1'
    APP_PORT = '8080'
    REFRESH_SEC_KEY = '21345'
    ACCESS_SEC_KEY = '34213'
    REFRESH_EXP_MIN = 3000
    ACCESS_EXP_MIN = 200
