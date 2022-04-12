import os

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

    #DB_DROP_AND_CREATE_ALL = parse_var_env('DB_DROP_AND_CREATE_ALL') or False
    #GENERATE_FAKE_DATA = parse_var_env('GENERATE_FAKE_DATA') or False

    ELASTICSEARCH_URL = parse_var_env('ELASTICSEARCH_URL')
    INDEX_PREFIX = parse_var_env('INDEX_PREFIX')
    DEFAULT_INDEX_NAME = parse_var_env('DEFAULT_INDEX_NAME')
    SEARCH_RESULT_PER_PAGE =  parse_var_env('SEARCH_RESULT_PER_PAGE')

    #ASSETS_DEBUG = parse_var_env('ASSETS_DEBUG') or False
    #SCSS_STATIC_DIR = os.path.join(basedir, "app ", "static", "css")
    #SCSS_ASSET_DIR = os.path.join(basedir, "app", "assets", "scss")
    CSRF_ENABLED = parse_var_env('CSRF_ENABLED')

    APP_URL_PREFIX = parse_var_env('APP_URL_PREFIX')
    API_VERSION = parse_var_env('API_VERSION')
    API_URL_PREFIX = parse_var_env('API_URL_PREFIX')
    IIIF_URL_PREFIX = parse_var_env('IIIF_URL_PREFIX')

    # Flask-User settings
    USER_APP_NAME = parse_var_env("USER_APP_NAME") or "Lettres"     # Shown in and email templates and page footers

    # Flask-Mail settings
    MAIL_SERVER = 'relay.huma-num.fr'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'lettres@chartes.psl.eu'

    JWT_SECRET_KEY = parse_var_env('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = ['cookies', 'headers']
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_COOKIE_SECURE = True
    JWT_IDENTITY_CLAIM = 'sub'

    LOCAL_TMP_FOLDER = parse_var_env('LOCAL_TMP_FOLDER')
    SFTP_IIIF_HOST = parse_var_env('SFTP_IIIF_HOST')
    SFTP_IIIF_USERNAME = parse_var_env('SFTP_IIIF_USERNAME')
    SFTP_IIIF_PASSWORD = parse_var_env('SFTP_IIIF_PASSWORD')
    SFTP_IIIF_DEFAULT_MANIFEST_PATH = parse_var_env('SFTP_IIIF_DEFAULT_MANIFEST_PATH')
    SFTP_IIIF_DEFAULT_COLLECTION_PATH = parse_var_env('SFTP_IIIF_DEFAULT_COLLECTION_PATH')

    IIIF_MANIFEST_ENDPOINT = parse_var_env('IIIF_MANIFEST_ENDPOINT')
    IIIF_COLLECTION_ENDPOINT = parse_var_env('IIIF_COLLECTION_ENDPOINT')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):

    ENV = 'development'

    @staticmethod
    def init_app(app):
        print('THIS APP IS IN DEV MODE. YOU SHOULD NOT SEE THIS IN PRODUCTION.')
        with app.app_context():
            db_url = app.config["SQLALCHEMY_DATABASE_URI"]



class TestConfig(Config):
    ENV = 'testing'

    @staticmethod
    def init_app(app):
        print('THIS APP IS IN TEST MODE. YOU SHOULD NOT SEE THIS IN PRODUCTION.')

config = {
    "dev": DevelopmentConfig,
    "prod": Config,
    "test": TestConfig
}
