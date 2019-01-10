import pprint
from elasticsearch import Elasticsearch
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, inspect
from sqlalchemy.engine import Engine

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


class ModelChangeEvent(object):
    def __init__(self, app, session, *callbacks):
        self.app = app
        self.model_changes = {}
        self.callbacks = callbacks
        self.session = session
        self.register_events(session)

    def record_ops(self, session, flush_context=None, instances=None):
        for targets, operation in ((session.new, 'insert'), (session.dirty, 'update'), (session.deleted, 'delete')):
            for target in targets:
                state = inspect(target)
                key = state.identity_key if state.has_identity else id(target)
                self.model_changes[key] = (target.id, target, operation)

    def after_commit(self, session):
        if self.model_changes:
            changes = list(self.model_changes.values())

            for callback in self.callbacks:
                callback(changes=changes)

            self.model_changes.clear()

    def after_rollback(self, session):
        self.model_changes.clear()

    def register_events(self, session):
        event.listen(session, 'before_flush', self.record_ops)
        event.listen(session, 'before_commit', self.record_ops)
        event.listen(session, 'after_commit', self.after_commit)
        event.listen(session, 'after_rollback', self.after_rollback)


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
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config['ELASTICSEARCH_URL'] else None

    # Hook elasticsearch to the session
    from app.search import SearchIndexManager
    app.mce = ModelChangeEvent(app, db.session, SearchIndexManager.reindex_resources)

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
    from app.api.collection.routes import register_collection_role_api_urls
    from app.api.institution.routes import register_institution_role_api_urls
    from app.api.language.routes import register_language_role_api_urls
    from app.api.image.routes import register_image_api_urls
    from app.api.note.routes import register_note_api_urls
    from app.api.user.routes import register_user_api_urls
    from app.api.user_role.routes import register_user_role_api_urls
    from app.api.whitelist.routes import register_whitelist_api_urls
    from app.api.witness.routes import register_witness_api_urls

    with app.app_context():
        # generate routes for the API
        register_correspondent_api_urls(app)
        register_correspondent_has_role_api_urls(app)
        register_correspondent_role_api_urls(app)
        register_document_api_urls(app)
        register_institution_role_api_urls(app)
        register_language_role_api_urls(app)
        register_image_api_urls(app)
        register_note_api_urls(app)
        register_user_api_urls(app)
        register_user_role_api_urls(app)
        register_whitelist_api_urls(app)
        register_collection_role_api_urls(app)
        register_witness_api_urls(app)

        # generate search endpoint
        app.api_url_registrar.register_search_route()

    app.register_blueprint(app_bp)
    app.register_blueprint(api_bp)

    return app
