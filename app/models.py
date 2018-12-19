from app import db

from app.search import add_to_index, remove_from_index, query_index

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


class SearchableMixin(object):
    __searchable__ = []

    @classmethod
    def search(cls, expression, fields=None, page=None, per_page=None, index=None):

        # by default, search on the model table
        # custom index allow to use multiple indexes: index="table1,table2,table3..."
        if index is None:
            index = cls.__tablename__

        # perform the query
        print(page, per_page)
        results, total = query_index(index=index, query=expression,
                                     fields=fields, page=page, per_page=per_page)
        print(expression, results, total)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        # TODO recuperer les indexes et faire les bonnes requetes/jointures
        ids = [r.id for r in results]

        if len(ids) == 0:
            return cls.query.filter_by(id=0), 0

        for i in range(len(ids)):
            when.append((ids[i], i))

        # print("test")
        # print("when:", when)
        # for idx in index.split(","):
        #    obj = db.session.query(MODELS_HASH_TABLE[idx]).filter()
        #    print(idx, obj)
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


class Collection(SearchableMixin, db.Model):
    """ Une collection: un regroupement de lettres.

    """

    __tablename__ = 'collection'
    __table_args__ = (
        db.UniqueConstraint('title',  name='_collection_title_uc'),
    )
    __searchable__ = ['title']

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(400))


class Document(SearchableMixin, db.Model):
    """Un document transcrit – ici, une lettre.

    """

    __tablename__ = 'document'
    __searchable__ = ['title']

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    witness_label = db.Column(db.String(200))
    institution_id = db.Column(db.Integer, db.ForeignKey('institution.id'), index=True)
    classification_mark = db.Column(db.String(100))
    tradition_id = db.Column(db.Integer, db.ForeignKey('tradition.id'), index=True)
    argument = db.Column(db.Text)
    creation = db.Column(db.String)
    creation_label = db.Column(db.String)
    location_date_label = db.Column(db.String)
    location_date_ref = db.Column(db.String)
    prev_document_id = db.Column(db.Integer, db.ForeignKey('document.id'), index=True)
    transcription = db.Column(db.Text)
    date_insert = db.Column(db.String)
    date_update = db.Column(db.String)
    is_published = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    whitelist_id = db.Column(db.Integer, db.ForeignKey('whitelist.id'), index=True)

    # relationships
    images = db.relationship("Image", backref="document")
    notes = db.relationship("Note", backref="document")
    owner = db.relationship("User", backref="owned_documents")

    languages = db.relationship("Language",
                                secondary=association_document_has_language,
                                backref=db.backref('documents', ))

    collections = db.relationship("Collection",
                                secondary=association_document_has_collection,
                                backref=db.backref('documents', ))

    # relation unaire (liste ? ordonnée ?)
    next_document = db.relationship("Document", backref=db.backref('prev_document', remote_side=id), uselist=False)


class Note(SearchableMixin, db.Model):
    """ Note (appel point) de transcription non typée ; contenu riche """
    __tablename__ = 'note'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String, nullable=False)
    label = db.Column(db.String(45))
    document_id = db.Column(db.Integer, db.ForeignKey('document.id', ondelete='CASCADE'), nullable=False, index=True)


class Institution(SearchableMixin, db.Model):
    """ Institution de conservation du témoin édité """
    __tablename__ = "institution"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45))
    ref = db.Column(db.String(200))

    # relationships
    documents = db.relationship("Document", backref="institution")


class Image(SearchableMixin, db.Model):
    """ Liens aux images du témoin """
    __tablename__ = "image"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    canvas_idx = db.Column(db.Integer, nullable=False)
    manifest_url = db.Column(db.String(200))
    document_id = db.Column(db.Integer, db.ForeignKey('document.id', ondelete='CASCADE'), index=True)


class Language(SearchableMixin, db.Model):
    """ Langue(s) de la lettre transcrite """
    __tablename__ = 'language'
    __table_args__ = (
        db.UniqueConstraint('code',  name='_language_code_uc'),
    )
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(3), nullable=False)
    label = db.Column(db.String(45))


class Tradition(SearchableMixin, db.Model):
    """ Mode de tradition du témoin transcrit (original, copie, etc.) """
    __tablename__ = "tradition"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(200))

    # relationships
    documents = db.relationship("Document", backref="tradition")


class Correspondent(SearchableMixin, db.Model):
    """ Correspondants d’une lettre (expéditeur(s) et destinataire(s)) """
    __tablename__ = 'correspondent'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    key = db.Column(db.String)
    ref = db.Column(db.String)


class CorrespondentRole(SearchableMixin, db.Model):
    """ Rôle des correspondants (expéditeur, destinataire) """
    __tablename__ = 'correspondent_role'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100))


class CorrespondentHasRole(SearchableMixin, db.Model):
    __tablename__ = 'correspondent_has_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    __table_args__ = (
        db.UniqueConstraint('correspondent_id', 'document_id', name='_correspondent_has_role_document_uc'),
    )

    correspondent_id = db.Column(db.Integer, db.ForeignKey('correspondent.id', ondelete='CASCADE'), nullable=False)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id', ondelete='CASCADE'), nullable=False)
    correspondent_role_id = db.Column(db.Integer, db.ForeignKey('correspondent_role.id', ondelete='CASCADE'), nullable=False)

    correspondent = db.relationship("Correspondent", backref=db.backref("correspondents_having_roles"), single_parent=True)
    document = db.relationship("Document", backref=db.backref("correspondents_having_roles"), single_parent=True)
    correspondent_role = db.relationship("CorrespondentRole", backref=db.backref("correspondents_having_roles"), single_parent=True)


class User(SearchableMixin, db.Model):
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

    role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'), nullable=False, index=True)


class UserRole(SearchableMixin, db.Model):
    """ Rôle des utilisateurs (administrateur ou contributeur) """
    __tablename__ = 'user_role'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(200))

    # relationships
    users = db.relationship(User, backref="role")


class UserInvitation(db.Model):
    __tablename__ = 'user_invitation'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # UserInvitation email information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    email = db.Column(db.String(255, collation='NOCASE'), nullable=False)
    # save the user of the invitee
    invited_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))


class Whitelist(SearchableMixin, db.Model):
    """ Liste d’utilisateur(s) """
    __tablename__ = 'whitelist'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(45))

    # relationships
    documents = db.relationship(Document, backref="whitelist")
    users = db.relationship(User,
                            secondary=association_whitelist_has_user,
                            backref=db.backref('whitelists', ))
