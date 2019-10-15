import os


APP_CONFIG = {
    'secret_key': os.getenv('SECRET_KEY', 'TEST-SECRET-KEY'),
    'debug': True,
    'testing': True,
    'movie_pagination': 5
}

DATABASE = {
    'drivername': 'postgres',
    'host': os.getenv('DATABASE_HOSTNAME', 'localhost'),
    'port': os.getenv('DATABASE_PORT', '5432'),
    'username': os.getenv('DATABASE_USERNAME', 'postgres'),
    'password': os.getenv('DATABASE_PASSWORD', 'postgres'),
    'database': os.getenv('DATABASE_DB_NAME', 'moviedb')
}


class Config(object):
    DEBUG = APP_CONFIG.get('debug')
    TESTING = APP_CONFIG.get('testing')
    SECRET_KEY = APP_CONFIG.get('secret_key')

    SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s:%s/%s' % (DATABASE.get('username'),
                                                               DATABASE.get('password'),
                                                               DATABASE.get('host'),
                                                               DATABASE.get('port'),
                                                               DATABASE.get('database'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
