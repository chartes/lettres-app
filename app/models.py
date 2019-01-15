from sqlalchemy import Enum

from app import db

association_document_has_language = db.Table('document_has_language',
                                             db.Column('document_id', db.Integer, db.ForeignKey('document.id'),
                                                       primary_key=True),
                                             db.Column('language_id', db.Integer, db.ForeignKey('language.id'),
                                                       primary_key=True)
                                             )

association_document_has_collection = db.Table('document_has_collection',
                                             db.Column('document_id', db.Integer, db.ForeignKey('document.id'),
                                                       primary_key=True),
                                             db.Column('collection_id', db.Integer, db.ForeignKey('collection.id'),
                                                       primary_key=True)
                                             )

association_whitelist_has_user = db.Table('whitelist_has_user',
                                          db.Column('whitelist_id', db.Integer, db.ForeignKey('whitelist.id'),
                                                    primary_key=True),
                                          db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
                                          )


class Collection(db.Model):
    """ Une collection: un regroupement de lettres.

    """

    __tablename__ = 'collection'
    __table_args__ = (
        db.UniqueConstraint('title',  name='_collection_title_uc'),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(400))


class Document(db.Model):
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

    prev_document_id = db.Column(db.Integer, db.ForeignKey('document.id'), index=True)
    transcription = db.Column(db.Text)
    date_insert = db.Column(db.String)
    date_update = db.Column(db.String)
    is_published = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    whitelist_id = db.Column(db.Integer, db.ForeignKey('whitelist.id'), index=True)

    # relationships
    notes = db.relationship("Note", backref="document", cascade="all, delete-orphan")
    witnesses = db.relationship("Witness", backref="document", cascade="all, delete-orphan")

    owner = db.relationship("User", backref="owned_documents")

    languages = db.relationship("Language",
                                secondary=association_document_has_language,
                                backref=db.backref('documents', ))

    collections = db.relationship("Collection",
                                secondary=association_document_has_collection,
                                backref=db.backref('documents', ))

    # relation unaire (liste ? ordonnée ?)
    next_document = db.relationship("Document", backref=db.backref('prev_document', remote_side=id), uselist=False)


class Note(db.Model):
    """ Note (appel point) de transcription non typée ; contenu riche """
    __tablename__ = 'note'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String, nullable=False)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id', ondelete='CASCADE'), nullable=False, index=True)


TRADITION_VALUES = ('autographe', 'original', 'minute', 'copie', 'édition')
WITNESS_STATUS_VALUES = ('base', 'autre')


class Witness(db.Model):
    """ Témoin """
    __tablename__ = "witness"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id', ondelete='CASCADE'), nullable=False, index=True)

    content = db.Column(db.String, nullable=False, index=True)
    tradition = db.Column('tradition', Enum(*TRADITION_VALUES), index=True)
    status = db.Column('status', Enum(*WITNESS_STATUS_VALUES), index=True)
    institution_id = db.Column(db.Integer, db.ForeignKey('institution.id'))
    classification_mark = db.Column(db.String(100))


class Institution(db.Model):
    """ Institution de conservation """
    __tablename__ = "institution"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45))
    ref = db.Column(db.String(200))

    # relationships
    witnesses = db.relationship("Witness", backref="institution")


class Image(db.Model):
    """ Liens aux images du témoin """
    __tablename__ = "image"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    witness_id = db.Column(db.Integer, db.ForeignKey('witness.id', ondelete='CASCADE'), index=True)

    canvas_id = db.Column(db.String, nullable=False)
    index = db.Column(db.Integer, default=1)

    witness = db.relationship("Witness", backref="images")


class Language(db.Model):
    """ Langue(s) de la lettre transcrite """
    __tablename__ = 'language'
    __table_args__ = (
        db.UniqueConstraint('code',  name='_language_code_uc'),
    )
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(3), nullable=False)
    label = db.Column(db.String(45))


class Correspondent(db.Model):
    """ Correspondants d’une lettre (expéditeur(s) et destinataire(s)) """
    __tablename__ = 'correspondent'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    key = db.Column(db.String)
    ref = db.Column(db.String)


class CorrespondentRole(db.Model):
    """ Rôle des correspondants (expéditeur, destinataire) """
    __tablename__ = 'correspondent_role'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100))


class CorrespondentHasRole(db.Model):
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


class User(db.Model):
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

    roles = db.relationship('UserRole', secondary='user_has_role')

    @staticmethod
    def add_default_users():
        admin = UserRole.query.filter(UserRole.name == "admin").first()
        db.session.add(User(username="admin", email="admin.lettres@chartes.psl.eu", roles=[admin]))


class UserRole(db.Model):
    """ Rôle des utilisateurs (administrateur ou contributeur) """
    __tablename__ = 'user_role'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(200))

    @staticmethod
    def add_default_roles():
        db.session.add(UserRole(name="admin", description="Administrator"))
        db.session.add(UserRole(name="contributor", description="Contributor"))


class UserHasRole(db.Model):
    __tablename__ = 'user_has_role'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('user_role.id', ondelete='CASCADE'))


class UserInvitation(db.Model):
    __tablename__ = 'user_invitation'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # UserInvitation email information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    email = db.Column(db.String(255, collation='NOCASE'), nullable=False)
    # save the user of the invitee
    invited_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))


class Whitelist(db.Model):
    """ Liste d’utilisateur(s) """
    __tablename__ = 'whitelist'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    label = db.Column(db.String(45))

    # relationships
    documents = db.relationship(Document, backref="whitelist")
    owner = db.relationship(User, foreign_keys=[owner_id])
    users = db.relationship(User,
                            secondary=association_whitelist_has_user,
                            backref=db.backref('whitelists', ))
