from app.api.changelog.facade import ChangelogFacade
from app.api.collection.facade import CollectionFacade
from app.api.person.facade import PersonFacade
from app.api.person_has_role.facade import PersonHasRoleFacade
from app.api.person_role.facade import PersonRoleFacade
from app.api.document.facade import DocumentFacade, DocumentSearchFacade, DocumentBookmarkFacade, DocumentStatusFacade
from app.api.image.facade import ImageFacade
from app.api.institution.facade import InstitutionFacade
from app.api.language.facade import LanguageFacade
from app.api.note.facade import NoteFacade
from app.api.placename.facade import PlacenameFacade
from app.api.placename_has_role.facade import PlacenameHasRoleFacade
from app.api.placename_role.facade import PlacenameRoleFacade
from app.api.user.facade import UserFacade
from app.api.user_role.facade import UserRoleFacade
from app.api.witness.facade import WitnessFacade
from app.api.lock.facade import LockFacade
from app.models import Collection, Person, PersonHasRole, PersonRole, Document, Image, Institution, \
    Language, Note, User, UserRole, Witness, Lock, Placename, PlacenameHasRole, PlacenameRole

_FACADES = {

    # immediate facades
    "bookmark": DocumentBookmarkFacade,
    "status": DocumentStatusFacade,

    Collection.__tablename__: {
        "default": CollectionFacade,
        "search": CollectionFacade,
    },
    Person.__tablename__: {
        "default": PersonFacade,
        "search": PersonFacade,
    },
    Placename.__tablename__: {
        "default": PlacenameFacade,
        "search": PlacenameFacade,
    },
    PlacenameHasRole.__tablename__: {
        "default": PlacenameHasRoleFacade,
        "search": PlacenameHasRoleFacade,
    },
    PlacenameRole.__tablename__: {
        "default": PlacenameRoleFacade,
        "search": PlacenameRoleFacade,
    },
    PersonHasRole.__tablename__: {
        "default": PersonHasRoleFacade,
        "search": PersonHasRoleFacade,
    },
    PersonRole.__tablename__: {
        "default": PersonRoleFacade,
        "search": PersonRoleFacade,
    },
    Document.__tablename__: {
        "default": DocumentFacade,
        "search": DocumentSearchFacade,
        "status": DocumentStatusFacade,
    },
    Image.__tablename__: {
        "default": ImageFacade,
        "search": ImageFacade,
    },
    Institution.__tablename__: {
        "default": InstitutionFacade,
        "search": InstitutionFacade,
    },
    Language.__tablename__: {
        "default": LanguageFacade,
        "search": LanguageFacade,
    },
    Note.__tablename__: {
        "default": NoteFacade,
        "search": NoteFacade,
    },
    User.__tablename__: {
        "default": UserFacade,
        "search": UserFacade,
    },
    UserRole.__tablename__: {
        "default": UserRoleFacade,
        "search": UserRoleFacade,
    },
    Witness.__tablename__: {
        "default": WitnessFacade,
        "search": WitnessFacade,
    },
    Lock.__tablename__: {
        "default": LockFacade,
        "search": LockFacade,
    },
    "change": {
        "default": ChangelogFacade,
        "search": ChangelogFacade,
    },
}


class JSONAPIFacadeManager(object):
    FACADE_TYPES = ("default", "search")

    IDMapper = {

    }

    FACADES = _FACADES

    @staticmethod
    def get_facade_class_from_name(rel, name):
        try:
            return JSONAPIFacadeManager.FACADES[rel][name]
        except Exception as e:
            print(e)
            print("Facade %s unknown" % name)
            return JSONAPIFacadeManager.FACADES[name]

    @staticmethod
    def get_facade_class(obj, facade_type="default"):
        try:
            return JSONAPIFacadeManager.FACADES[obj.__tablename__][facade_type]
        except Exception as e:
            print(e)
            print("Facade %s %s unknown" % (obj, facade_type))
            return None

    @staticmethod
    def get_facade_class_from_facade_type(t, facade_type="default"):
        t = t.replace("-", "_")
        try:
            return JSONAPIFacadeManager.FACADES[t][facade_type]
        except Exception as e:
            print("Facade %s %s unknown" % (t, facade_type))
            return None
