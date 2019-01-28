import datetime
from flask_user import UserMixin
from sqlalchemy import Enum, DateTime, func
from sqlalchemy.ext.declarative import declared_attr

from app import db


def datetime_to_str(d):
    return d.strftime("%Y-%m-%d %H:%M:%S") if d else None


association_document_has_language = db.Table('document_has_language',
    db.Column('document_id', db.Integer, db.ForeignKey('document.id'), primary_key=True),
    db.Column('language_id', db.Integer, db.ForeignKey('language.id'), primary_key=True)
)

association_document_has_collection = db.Table('document_has_collection',
    db.Column('document_id', db.Integer, db.ForeignKey('document.id'), primary_key=True),
    db.Column('collection_id', db.Integer, db.ForeignKey('collection.id'), primary_key=True)
)

association_user_has_bookmark = db.Table('user_has_bookmark',
    db.Column('doc_id', db.Integer, db.ForeignKey('document.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

association_user_has_role = db.Table('user_has_role',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('user_role.id'), primary_key=True)
)


class ChangesMixin:

    __tablename__ = "ChangesMixin"

    @declared_attr
    def changes(self):
        return db.relationship("Changelog",
                               primaryjoin="and_({0}.id==foreign(Changelog.object_id),"
                                           "Changelog.object_type=='{1}')".format(self.__name__,  self.__tablename__))


class Document(db.Model, ChangesMixin):
    """Un document transcrit – ici, une lettre.

    """

    __tablename__ = 'document'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(200), nullable=False)
    argument = db.Column(db.Text)
    creation = db.Column(db.String)
    creation_not_after = db.Column(db.String)
    creation_label = db.Column(db.String)
    location_date_from_ref = db.Column(db.String)
    location_date_to_ref = db.Column(db.String)
    transcription = db.Column(db.Text)
    prev_document_id = db.Column(db.Integer, db.ForeignKey('document.id'), index=True)
    is_published = db.Column(db.Boolean, index=True)

    # relationships
    notes = db.relationship("Note", backref="document", cascade="all, delete-orphan")
    witnesses = db.relationship("Witness", backref="document", cascade="all, delete-orphan")
    languages = db.relationship("Language",
                                secondary=association_document_has_language,
                                backref=db.backref('documents', ))
    collections = db.relationship("Collection",
                                secondary=association_document_has_collection,
                                backref=db.backref('documents', ))
    next_document = db.relationship("Document", backref=db.backref('prev_document', remote_side=id), uselist=False)

    locks = db.relationship("Lock",
                            primaryjoin="and_(Document.id==foreign(Lock.object_id),"
                                        "Lock.object_type=='{0}',"
                                        "Lock.expiration_date > {1})".format(__tablename__, 'func.current_date()'))


class Collection(db.Model, ChangesMixin):
    """ Une collection: un regroupement de lettres.

    """

    __tablename__ = 'collection'
    __table_args__ = (
        db.UniqueConstraint('title',  name='_collection_title_uc'),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(400))


class Note(db.Model, ChangesMixin):
    """ Note (appel point) de transcription non typée ; contenu riche """
    __tablename__ = 'note'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String, nullable=False)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id', ondelete='CASCADE'), nullable=False, index=True)


TRADITION_VALUES = ('autographe', 'original', 'minute', 'copie', 'édition')
WITNESS_STATUS_VALUES = ('base', 'autre')


class Witness(db.Model, ChangesMixin):
    """ Témoin """
    __tablename__ = "witness"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id', ondelete='CASCADE'), nullable=False, index=True)
    num = db.Column(db.Integer, nullable=False, server_default='1')  # ordre d'importance du témoin
    content = db.Column(db.String, nullable=False, index=True)
    tradition = db.Column('tradition', Enum(*TRADITION_VALUES), index=True)
    status = db.Column('status', Enum(*WITNESS_STATUS_VALUES), index=True)
    institution_id = db.Column(db.Integer, db.ForeignKey('institution.id'))
    classification_mark = db.Column(db.String(100))


class Institution(db.Model, ChangesMixin):
    """ Institution de conservation """
    __tablename__ = "institution"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45))
    ref = db.Column(db.String(200))

    # relationships
    witnesses = db.relationship("Witness", backref="institution")


class Image(db.Model, ChangesMixin):
    """ Liens aux images du témoin """
    __tablename__ = "image"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    witness_id = db.Column(db.Integer, db.ForeignKey('witness.id', ondelete='CASCADE'), index=True)

    canvas_id = db.Column(db.String, nullable=False)
    order_num = db.Column(db.Integer, server_default='1')

    witness = db.relationship("Witness", backref="images")


class Language(db.Model, ChangesMixin):
    """ Langue(s) de la lettre transcrite """
    __tablename__ = 'language'
    __table_args__ = (
        db.UniqueConstraint('code',  name='_language_code_uc'),
    )
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(3), nullable=False)
    label = db.Column(db.String(45))


# ====================================
# CORRESPONDENT STUFF
# ====================================


class Correspondent(db.Model, ChangesMixin):
    """ Correspondants d’une lettre (expéditeur(s) et destinataire(s)) """
    __tablename__ = 'correspondent'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    key = db.Column(db.String)
    ref = db.Column(db.String)


class CorrespondentRole(db.Model, ChangesMixin):
    """ Rôle des correspondants (expéditeur, destinataire) """
    __tablename__ = 'correspondent_role'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100))


class CorrespondentHasRole(db.Model, ChangesMixin):
    __tablename__ = 'correspondent_has_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    __table_args__ = (
        db.UniqueConstraint('correspondent_id', 'document_id', name='_correspondent_has_role_document_uc'),
    )

    correspondent_id = db.Column(db.Integer, db.ForeignKey('correspondent.id', ondelete='CASCADE'), nullable=False)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id', ondelete='CASCADE'), nullable=False)
    correspondent_role_id = db.Column(db.Integer, db.ForeignKey('correspondent_role.id', ondelete='CASCADE'), nullable=False)

    correspondent = db.relationship("Correspondent", backref=db.backref("correspondents_having_roles"), single_parent=True)
    document = db.relationship("Document", backref=db.backref("correspondents_having_roles", cascade="all, delete-orphan"), single_parent=True)
    correspondent_role = db.relationship("CorrespondentRole", backref=db.backref("correspondents_having_roles"), single_parent=True)


# ====================================
# USER STUFF
# ====================================


class User(db.Model, UserMixin):
    """ Utilisateur """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # User authentication information
    username = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False, server_default='')

    # User email information
    email = db.Column(db.String(), nullable=False, unique=True)
    email_confirmed_at = db.Column('confirmed_at', db.DateTime())

    # User information
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column('firstname', db.String(), nullable=False, server_default='')
    last_name = db.Column('lastname', db.String(), nullable=False, server_default='')

    roles = db.relationship('UserRole', secondary=association_user_has_role)
    bookmarked_documents = db.relationship("Document", secondary=association_user_has_bookmark)

    @staticmethod
    def add_default_users():
        password = "pbkdf2:sha256:50000$RyjGxAYv$02c62c497306be557eb4080a432c466453f297eb9dbfb62dc0160fe376f22689" # Lettres2019!
        admin = UserRole.query.filter(UserRole.name == "admin").first()
        contributor = UserRole.query.filter(UserRole.name == "contributor").first()

        if not User.query.filter(User.username == "admin").first():
            db.session.add(User(username="admin",
                                password=password,
                                email="admin.lettres@chartes.psl.eu",
                                active=True,
                                email_confirmed_at=datetime.datetime.now(),
                                roles=[admin, contributor]))
        if not User.query.filter(User.username == "contributor").first():
            db.session.add(User(username="contributor",
                                password=password,
                                email="contributor.lettres@chartes.psl.eu",
                                active=True,
                                email_confirmed_at=datetime.datetime.now(),
                                roles=[contributor]))

    def to_json(self):
        return {
            "username": self.username,
            "roles": [r.name for r in self.roles]
        }


class UserRole(db.Model):
    """ Rôle des utilisateurs (administrateur ou contributeur) """
    __tablename__ = 'user_role'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(200))

    @staticmethod
    def add_default_roles():
        if not UserRole.query.filter(UserRole.name == "admin").first():
            admin_role = UserRole(name="admin", description="Administrateur")
            db.session.add(admin_role)
        if not UserRole.query.filter(UserRole.name == "contributor").first():
            contributor_role = UserRole(name="contributor", description="Contributeur")
            db.session.add(contributor_role)


class UserInvitation(db.Model):
    __tablename__ = 'user_invitation'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # UserInvitation email information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    email = db.Column(db.String(255, collation='NOCASE'), nullable=False)
    # save the user of the invitee
    invited_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))


# ====================================
# LOCKS
# ====================================

LOCK_OBJECT_TYPES = [o.__tablename__ for o in (
    Document,
)]


class Lock(db.Model):
    """ Table des verrous """
    __tablename__ = "lock"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    object_type = db.Column(db.String, Enum(*LOCK_OBJECT_TYPES), index=True)
    object_id = db.Column(db.Integer, nullable=False, index=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_date = db.Column(DateTime(timezone=True), server_default=func.now())
    expiration_date = db.Column(DateTime(timezone=True), default=lambda: datetime.datetime.now() + datetime.timedelta(days=7))

    description = db.Column(db.String, nullable=True)

    user = db.relationship('User', backref=db.backref("locks", uselist=True), cascade="all, delete-orphan", single_parent=True)


# ====================================
# CHANGE LOG
# ====================================

CHANGELOG_OBJECT_TYPES = [o.__tablename__ for o in (
    Document, Collection, Correspondent, CorrespondentHasRole, CorrespondentRole,
    Image, Institution, Language, Note, Witness, Lock
)] + ['document_has_language', 'document_has_collection']


class Changelog(db.Model):
    """ Historique des modifications """
    __tablename__ = "changelog"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    object_type = db.Column(db.String, Enum(*CHANGELOG_OBJECT_TYPES), index=True)
    object_id = db.Column(db.Integer, nullable=False, index=True)

    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    event_date = db.Column(DateTime(timezone=True), server_default=func.now())
    description = db.Column(db.String, nullable=True)

    user = db.relationship('User', backref=db.backref("changes", uselist=True), cascade="all, delete-orphan", single_parent=True)
