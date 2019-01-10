from app.api.collection.facade import CollectionFacade
from app.api.correspondent.facade import CorrespondentFacade
from app.api.correspondent_has_role.facade import CorrespondentHasRoleFacade
from app.api.correspondent_role.facade import CorrespondentRoleFacade
from app.api.document.facade import DocumentFacade
from app.api.image.facade import ImageFacade
from app.api.institution.facade import InstitutionFacade
from app.api.language.facade import LanguageFacade
from app.api.note.facade import NoteFacade
from app.api.user.facade import UserFacade
from app.api.user_role.facade import UserRoleFacade
from app.api.whitelist.facade import WhitelistFacade
from app.api.witness.facade import WitnessFacade
from app.models import Collection, Correspondent, CorrespondentHasRole, CorrespondentRole, Document, Image, Institution, \
    Language, Note, User, UserRole, Whitelist, Witness


class JSONAPIFacadeManager(object):

    FACADES = {
        Collection.__name__: {
            "default": CollectionFacade,
            "search": CollectionFacade,
        },
        Correspondent.__name__: {
            "default": CorrespondentFacade,
            "search": CorrespondentFacade,
        },
        CorrespondentHasRole.__name__: {
            "default": CorrespondentHasRoleFacade,
            "search": CorrespondentHasRoleFacade,
        },
        CorrespondentRole.__name__: {
            "default": CorrespondentRoleFacade,
            "search": CorrespondentRoleFacade,
        },
        Document.__name__: {
            "default": DocumentFacade,
            "search": DocumentFacade,
        },
        Image.__name__: {
            "default": ImageFacade,
            "search": ImageFacade,
        },
        Institution.__name__: {
            "default": InstitutionFacade,
            "search": InstitutionFacade,
        },
        Language.__name__: {
            "default": LanguageFacade,
            "search": LanguageFacade,
        },
        Note.__name__: {
            "default": NoteFacade,
            "search": NoteFacade,
        },
        User.__name__: {
            "default": UserFacade,
            "search": UserFacade,
        },
        UserRole.__name__: {
            "default": UserRoleFacade,
            "search": UserRoleFacade,
        },
        Whitelist.__name__: {
            "default": WhitelistFacade,
            "search": WhitelistFacade,
        },
        Witness.__name__: {
            "default": WitnessFacade,
            "search": WitnessFacade,
        },
    }

    @staticmethod
    def get_facade_class(obj, facade_type="default"):
        try:
            return JSONAPIFacadeManager.FACADES[obj.__class__.__name__][facade_type]
        except KeyError as e:
            print("Facade %s %s unknown" % (obj.__class__.__name__, facade_type))
            return None