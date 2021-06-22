import json
from elasticsearch import Elasticsearch
from flask import Flask, Blueprint, url_for, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager
from flask_migrate import Migrate
from sqlalchemy import event, MetaData
from sqlalchemy.engine import Engine

from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash

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

api_bp = Blueprint('api_bp', __name__)
app_bp = Blueprint('app_bp', __name__, template_folder='templates', static_folder='static')


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


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

    #api_bp.url_prefix = app.config["API_URL_PREFIX"]
    app.debug = app.config["DEBUG"]

    db.init_app(app)
    config[config_name].init_app(app)
    #migrate = Migrate(app, db, render_as_batch=True)

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config['ELASTICSEARCH_URL'] else None

    """
    ========================================================
        Setup Flask-JWT-Extended
    ========================================================
    """
    app.jwt = JWTManager(app)

    from app.api.manifest.manifest_factory import ManifestFactory
    app.manifest_factory = ManifestFactory()

    # =====================================
    # Import models & app routes
    # =====================================

    from app import models
    from app import routes

    # =====================================
    # register api routes
    # =====================================
    CORS(api_bp, supports_credentials=True)

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

    with app.app_context():
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
        app.api_url_registrar.register_search_route()

    app.register_blueprint(app_bp)
    app.register_blueprint(api_bp)

    return app
