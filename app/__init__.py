import json
from elasticsearch import Elasticsearch
from flask import Flask, Blueprint, url_for, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager
from sqlalchemy import event
from sqlalchemy.engine import Engine

from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash

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

"""
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
"""

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

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config['ELASTICSEARCH_URL'] else None

    CORS(app, resources={r"*": {"origins": "*"}})

    from app.models import User
    from app.models import UserInvitation

    """
    ========================================================
        Setup Flask-User
    ========================================================
    """
    class CustomUserManager(UserManager):
        def customize(self, app):
            self.UserInvitationClass = UserInvitation
            self.email_manager._render_and_send_email_with_exceptions = self.email_manager._render_and_send_email

            def with_protection(*args, **kargs):
                try:
                    self.email_manager._render_and_send_email_with_exceptions(*args, **kargs)
                except Exception as e:
                    print(e)
            self.email_manager._render_and_send_email = with_protection

        def hash_password(self, password):
            return generate_password_hash(password.encode('utf-8'))

        def verify_password(self, password, password_hash):
            return check_password_hash(password_hash, password)

        def _endpoint_url(self, endpoint):
            return url_for(endpoint) if endpoint else url_for('app_bp.index')

    # Initialize Flask-User
    app.user_manager = CustomUserManager(app, db, UserClass=User, UserInvitationClass=UserInvitation)

    from flask_user import user_changed_username, user_confirmed_email, user_sent_invitation, user_registered

    def reindex_user(user):
        print("reindex user", user)
        from app.api.user.facade import UserFacade
        f_obj = UserFacade(url_prefix="", obj=user, with_relationships_data=False, with_relationships_links=False)
        f_obj.reindex("insert", propagate=False)

    @user_changed_username.connect_via(app)
    def user_changed_username(sender, **extra):
        reindex_user(extra['user'])

    @user_confirmed_email.connect_via(app)
    def user_confirmed_email(sender, **extra):
        reindex_user(extra['user'])

    @user_sent_invitation.connect_via(app)
    def user_sent_invitation(sender, **extra):
        reindex_user(extra['user'])

    @user_registered.connect_via(app)
    def user_registered(sender, **extra):
        reindex_user(extra['user'])

    """
    ========================================================
        Setup Flask-JWT-Extended
    ========================================================
    """
    app.jwt = JWTManager(app)

    # Create a function that will be called whenever create_access_token
    # is used. It will take whatever object is passed into the
    # create_access_token method, and lets us define what custom claims
    # should be added to the access token.
    @app.jwt.user_claims_loader
    def add_claims_to_access_token(user):
        return user["roles"]

    # Create a function that will be called whenever create_access_token
    # is used. It will take whatever object is passed into the
    # create_access_token method, and lets us define what the identity
    # of the access token should be.
    @app.jwt.user_identity_loader
    def user_identity_lookup(user):
        return user["username"]

    from app.api.manifest.manifest_factory import ManifestFactory
    app.manifest_factory = ManifestFactory()

    # =====================================
    # Import models & app routes
    # =====================================

    from app import models
    from app import routes

    @app.errorhandler(404)
    def handle_page_not_found(e):
        title = "Page non trouvée"
        content = "Le contenu que vous cherchez n'existe pas à cette adresse"
        template = render_template('errors/generic.html', title=title, content=content)
        return render_template('app/main.html', section="errors", data=json.dumps({'template': template})), 404

    @app.errorhandler(500)
    def handle_bad_request(e):
        title = "Erreur serveur"
        content = "Erreur interne du serveur."
        template = render_template('errors/generic.html', title=title, content=content)
        return render_template('app/main.html', section="errors", data=json.dumps({'template': template})), 500

    # =====================================
    # register api routes
    # =====================================

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

    def get_value(value, key):
        return json.loads(value).get(key)
    app.jinja_env.filters['get_value'] = get_value

    return app
