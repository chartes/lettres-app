import pprint
from elasticsearch import Elasticsearch
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
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

    def add_to_index(index, id, payload):
        print("ADD_TO_INDEX", index, id, payload)
        from flask import current_app
        current_app.elasticsearch.index(index=index, doc_type=index, id=id, body=payload)

    def remove_from_index(index, id):
        print("REMOVE_FROM_INDEX", index, id)
        from flask import current_app
        current_app.elasticsearch.delete(index=index, doc_type=index, id=id)

    def reindex_resources(changes):
        from flask import current_app
        from app.api.facade_manager import JSONAPIFacadeManager

        db.session = db.create_scoped_session()
        current_app.mce.register_events(db.session)

        print("CHANGES after commit:", changes)
        for target, op in changes:
            facade = JSONAPIFacadeManager.get_facade_class(target)
            f_obj, kwargs, errors = facade.get_resource_facade("", id=target.id)
            if op in ('insert', 'update'):
                for data in f_obj.get_data_to_index_when_added():
                    print(target, data)
                    add_to_index(**data)
            if op == 'delete':
                for data in f_obj.get_data_to_index_when_removed():
                    print(target, data)
                    remove_from_index(**data)

    from app.search import ModelChangeEvent
    app.mce = ModelChangeEvent(db.session, reindex_resources)

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
        register_collection_role_api_urls(app)

        # generate search endpoint
        app.api_url_registrar.register_search_route()

    app.register_blueprint(app_bp)
    app.register_blueprint(api_bp)



    return app
