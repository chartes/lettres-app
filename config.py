
import os
from sqlalchemy_utils import database_exists, create_database

basedir = os.path.abspath(os.path.dirname(__file__))


def parse_var_env(var_name):
    v = os.environ.get(var_name)
    if v == "True":
        v = True
    elif v == "False":
        v = False
    return v


class Config(object):
    SECRET_KEY = parse_var_env('SECRET_KEY')
    ENV ='production'
    DEBUG = parse_var_env('DEBUG') or False

    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(os.path.abspath(os.getcwd()), parse_var_env('DATABASE_URI'))
    SQLALCHEMY_TRACK_MODIFICATIONS = parse_var_env('SQLALCHEMY_TRACK_MODIFICATIONS') or False
    SQLALCHEMY_ECHO = parse_var_env('SQLALCHEMY_ECHO') or False
    SQLALCHEMY_RECORD_QUERIES = parse_var_env('SQLALCHEMY_RECORD_QUERIES') or False

    DB_DROP_AND_CREATE_ALL = parse_var_env('DB_DROP_AND_CREATE_ALL') or False
    GENERATE_FAKE_DATA = parse_var_env('GENERATE_FAKE_DATA') or False

    ELASTICSEARCH_URL = parse_var_env('ELASTICSEARCH_URL')

    ASSETS_DEBUG = parse_var_env('ASSETS_DEBUG') or False
    SCSS_STATIC_DIR = os.path.join(basedir, "app ", "static", "css")
    SCSS_ASSET_DIR = os.path.join(basedir, "app", "assets", "scss")
    CSRF_ENABLED = parse_var_env('CSRF_ENABLED')

    APP_URL_PREFIX = parse_var_env('APP_URL_PREFIX')
    API_VERSION = parse_var_env('API_VERSION')
    API_URL_PREFIX = parse_var_env('API_URL_PREFIX')


class DevelopmentConfig(Config):

    ENV = 'development'

    @staticmethod
    def init_app(app):
        print('THIS APP IS IN DEV MODE. YOU SHOULD NOT SEE THIS IN PRODUCTION.')
        with app.app_context():
            db_url = app.config["SQLALCHEMY_DATABASE_URI"]
            if not database_exists(db_url):
                create_database(db_url)
            else:
                pass


class TestConfig(Config):
    ENV = 'testing'

    DB_DROP_AND_CREATE_ALL = True
    GENERATE_FAKE_DATA = False


config = {
    "dev": DevelopmentConfig,
    "prod": Config,
    "test": TestConfig
}
