import pprint
from elasticsearch import Elasticsearch
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

from werkzeug.contrib.profiler import ProfilerMiddleware
from dotenv import load_dotenv

from app.api.response_factory import JSONAPIResponseFactory


# Initialize Flask extensions

db = SQLAlchemy()

api_bp = Blueprint('api_bp', __name__)
app_bp = Blueprint('app_bp', __name__, template_folder='templates', static_folder='static')


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class PrefixMiddleware(object):

    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):

        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)


def create_app(config_name="dev"):
    """ Create the application """
    app = Flask(__name__)
    if not isinstance(config_name, str):
        from config import config
        print("default config")
        app.config.from_object(config)
    else:
        print("Load environment variables for config '%s'" % config_name)
        # It is important to load the .env file before parsing the config file
        load_dotenv('%s.env' % config_name, verbose=True)
        from config import config
        app.config.from_object(config[config_name])

    app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=app.config["APP_URL_PREFIX"])
    app.debug = app.config["DEBUG"]

    db.init_app(app)
    config[config_name].init_app(app)
    #app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config['ELASTICSEARCH_URL'] else None

    # =====================================
    # Import models & app routes
    # =====================================

    from app import models
    from app import routes

    # =====================================
    # register api routes
    # =====================================

    from app.api.route_registrar import JSONAPIRouteRegistrar
    app.api_url_registrar = JSONAPIRouteRegistrar(app.config["API_VERSION"], app.config["API_URL_PREFIX"])

    from app.api import routes

    from app.api.correspondent.routes import register_correspondent_api_urls
    from app.api.correspondent_has_role.routes import register_correspondent_has_role_api_urls
    from app.api.correspondent_role.routes import register_correspondent_role_api_urls
    from app.api.document.routes import register_document_api_urls
    from app.api.tradition.routes import register_tradition_role_api_urls
    from app.api.institution.routes import register_institution_role_api_urls
    from app.api.language.routes import register_language_role_api_urls
    from app.api.image.routes import register_image_api_urls
    from app.api.note.routes import register_note_api_urls
    from app.api.user.routes import register_user_api_urls
    from app.api.user_role.routes import register_user_role_api_urls
    from app.api.whitelist.routes import register_whitelist_api_urls

    with app.app_context():
        # generate routes for the API
        register_correspondent_api_urls(app)
        register_correspondent_has_role_api_urls(app)
        register_correspondent_role_api_urls(app)
        register_document_api_urls(app)
        register_tradition_role_api_urls(app)
        register_institution_role_api_urls(app)
        register_language_role_api_urls(app)
        register_image_api_urls(app)
        register_note_api_urls(app)
        register_user_api_urls(app)
        register_user_role_api_urls(app)
        register_whitelist_api_urls(app)

    app.register_blueprint(app_bp)
    app.register_blueprint(api_bp)

    if app.config["DB_DROP_AND_CREATE_ALL"] and app.config["ENV"] != "production":
        print("Recreating database...")
        with app.app_context():
            db.drop_all()
            db.create_all()

            if app.config["GENERATE_FAKE_DATA"]:
                # === load some fake data
                from faker import Faker
                fake = Faker()
                fake.seed(12345)
                from db.fixtures.create_fake_data import create_fake_documents, create_fake_users
                print("Generating fake data...", end=" ", flush=True)
                create_fake_users(db, nb_users=5, fake=fake)
                create_fake_documents(db, nb_docs=20, nb_correspondents=10, fake=fake)
                print("done !")

    return app
