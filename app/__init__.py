import os
import pathlib

from elasticsearch import Elasticsearch
from flask import Flask, Blueprint
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, MetaData
from sqlalchemy.engine import Engine

from dotenv import load_dotenv

from app.api.response_factory import JSONAPIResponseFactory

# Initialize Flask extensions
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
mail = Mail()

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

# Without Prefix /ecco (also update in flask_app.py & in VUE_APP var_env):
# def create_app(config_name="dev", with_hardcoded_prefix=False):

# With Prefix /ecco (also update in flask_app.py & in VUE_APP var_env):
def create_app(config_name="dev", with_hardcoded_prefix=True):
    """ Create the application """
    app = Flask(__name__)
    if not isinstance(config_name, str):
        from config import config
        print("default config")
        app.config.from_object(config)
    else:
        print("Load environment variables for config '%s'" % config_name)
        # It is important to load the .env file before parsing the config file
        path = pathlib.Path(__file__).parent.parent.resolve()
        path = path / f"{config_name}.env"
        load_dotenv(path, verbose=True)
        from config import config
        app.config.from_object(config[config_name])

    app.debug = app.config["DEBUG"]

    def with_url_prefix(url):
        from flask import request
        return "".join((request.host_url[:-1], app.config['APP_URL_PREFIX'], url))

    app.with_url_prefix = with_url_prefix

    db.init_app(app)
    config[config_name].init_app(app)
    mail.init_app(app)

    print(app.config["SQLALCHEMY_DATABASE_URI"])

    # migrate = Migrate(app, db, render_as_batch=True)

    if with_hardcoded_prefix:
        app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=app.config["APP_URL_PREFIX"])

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config['ELASTICSEARCH_URL'] else None

    """
        ========================================================
              Setup Flask-JWT-Extended
        ========================================================
    """
    app.jwt = JWTManager(app)

    # Create a function that will be called whenever create_access_token
    # is used. It will take whatever object is passed into the
    # create_access_token method, and lets us define what the identity
    # of the access token should be.
    @app.jwt.user_identity_loader
    def user_identity_lookup(user):
        return user["email"]

    # Create a function that will be called whenever create_access_token
    # is used. It will take whatever object is passed into the
    # create_access_token method, and lets us define what custom claims
    # should be added to the access token.
    @app.jwt.additional_claims_loader
    def add_claims_to_access_token(user):
        return user["roles"]

    def get_current_user():
        import jwt
        from flask import request
        from app.models import User
        auth_headers = request.headers.get('Authorization', '').split()
        if len(auth_headers) == 2:
            token = auth_headers[1]
            data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms=["HS256"])
            return User.query.filter_by(email=data['sub']).first()
        else:
            return None

    app.get_current_user = get_current_user

    from app.api.manifest.manifest_factory import ManifestFactory
    app.manifest_factory = ManifestFactory()

    # =====================================
    # Import models & app routes
    # =====================================

    with app.app_context():
        from app import models
        from app import routes

        # =====================================
        # register api routes
        # =====================================
        CORS(app, supports_credentials=True)

        from app.api.route_registrar import JSONAPIRouteRegistrar
        app.api_url_registrar = JSONAPIRouteRegistrar(app.config["API_VERSION"], app.config["API_URL_PREFIX"])

        from app.api import routes

        from app.api.person.routes import register_person_api_urls
        from app.api.person_has_role.routes import register_person_has_role_api_urls
        from app.api.person_role.routes import register_person_role_api_urls
        from app.api.document.routes import register_document_api_urls
        from app.api.collection.routes import register_collection_role_api_urls
        from app.api.institution.routes import register_institution_role_api_urls
        from app.api.language.routes import register_language_role_api_urls
        from app.api.image.routes import register_image_api_urls
        from app.api.note.routes import register_note_api_urls
        from app.api.user.routes import register_user_api_urls
        from app.api.user_role.routes import register_user_role_api_urls
        from app.api.witness.routes import register_witness_api_urls
        from app.api.lock.routes import register_lock_api_urls
        from app.api.changelog.routes import register_changelog_api_urls
        from app.api.placename.routes import register_placename_api_urls
        from app.api.placename_has_role.routes import register_placename_has_role_api_urls
        from app.api.placename_role.routes import register_placename_role_api_urls

        # generate routes for the API
        register_person_api_urls(app)
        register_person_has_role_api_urls(app)
        register_person_role_api_urls(app)
        register_document_api_urls(app)
        register_institution_role_api_urls(app)
        register_language_role_api_urls(app)
        register_image_api_urls(app)
        register_note_api_urls(app)
        register_user_api_urls(app)
        register_user_role_api_urls(app)
        register_lock_api_urls(app)
        register_changelog_api_urls(app)
        register_collection_role_api_urls(app)
        register_witness_api_urls(app)
        register_placename_api_urls(app)
        register_placename_has_role_api_urls(app)
        register_placename_role_api_urls(app)

        # generate search endpoint
        app.api_url_registrar.register_count_route()
        app.api_url_registrar.register_search_route()

        #for rule in app.url_map.iter_rules():
        #    print(rule)
        title = app.config["UNSORTED_DOCUMENTS_COLLECTION_TITLE"]
        if not models.Collection.query.filter(models.Collection.title == title).all():
            print(f"unsorted documents collection '{title}' does not exist")
            print(f"creating unsorted documents collection '{title}' ...")
            unsorted_documents_collection = models.Collection(
                title=title,
                description="Lettres non associées à une collection",
                admin_id=1,
            )
            db.session.add(unsorted_documents_collection)
            db.session.commit()
            print(f"unsorted documents collection '{title}' has been successfully created")

    return app
