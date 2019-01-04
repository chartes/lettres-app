from app.api.abstract_facade import JSONAPIAbstractFacade
from app.models import Document


## decorator for test purposes
#def decorator_function_with_arguments(arg1, arg2, arg3):
#    def wrap(f):
#        print("Wrapping", f)
#
#        def wrapped_f(*args, **kwargs):
#            print("Inside wrapped_f()")
#            print(arg1, arg2, arg3)
#            res = f(*args, **kwargs)
#            return res
#
#        return wrapped_f
#
#    return wrap
#
#test_decorator = lambda *args, **kwargs: decorator_function_with_arguments(*args, **kwargs)
#


class DocumentFacade(JSONAPIAbstractFacade):
    """

    """
    TYPE = "document"
    TYPE_PLURAL = "documents"

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def get_resource_facade(url_prefix, id, **kwargs):
        e = Document.query.filter(Document.id == id).first()
        if e is None:
            kwargs = {"status": 404}
            errors = [{"status": 404, "title": "document %s does not exist" % id}]
        else:
            e = DocumentFacade(url_prefix, e, **kwargs)
            kwargs = {}
            errors = []
        return e, kwargs, errors

    @staticmethod
    def create_resource(model, obj_id, attributes, related_resources):
        if "last-update" in attributes:
            attributes["date_update"] = attributes.pop("last-update")
        return JSONAPIAbstractFacade.create_resource(model, obj_id, attributes, related_resources)

    def get_correspondents_having_roles_resource_identifiers(self):
        from app.api.correspondent_has_role.facade import CorrespondentHasRoleFacade
        return [] if self.obj.correspondents_having_roles is None else [
            CorrespondentHasRoleFacade.make_resource_identifier(c.id, CorrespondentHasRoleFacade.TYPE)
            for c in self.obj.correspondents_having_roles
        ]

    def get_correspondents_having_roles_resources(self):
        from app.api.correspondent_has_role.facade import CorrespondentHasRoleFacade
        return [] if self.obj.correspondents_having_roles is None else [
            CorrespondentHasRoleFacade(self.url_prefix, c, self.with_relationships_links,
                                       self.with_relationships_data).resource
            for c in self.obj.correspondents_having_roles
        ]

    def get_role_resource_identifiers(self):
        from app.api.correspondent_role.facade import CorrespondentRoleFacade
        return [] if self.obj.correspondents_having_roles is None else [
            CorrespondentRoleFacade.make_resource_identifier(c_h_r.correspondent_role.id, CorrespondentRoleFacade.TYPE)
            for c_h_r in self.obj.correspondents_having_roles
        ]

    def get_role_resources(self):
        from app.api.correspondent_role.facade import CorrespondentRoleFacade
        return [] if self.obj.correspondents_having_roles is None else [
            CorrespondentRoleFacade(self.url_prefix, c.correspondent_role, self.with_relationships_links,
                                    self.with_relationships_data).resource
            for c in self.obj.correspondents_having_roles
        ]

    def get_correspondent_resource_identifiers(self):
        from app.api.correspondent.facade import CorrespondentFacade
        return [] if self.obj.correspondents_having_roles is None else [
            CorrespondentFacade.make_resource_identifier(c_h_r.correspondent.id, CorrespondentFacade.TYPE)
            for c_h_r in self.obj.correspondents_having_roles
        ]

    def get_correspondent_resources(self):
        from app.api.correspondent.facade import CorrespondentFacade
        return [] if self.obj.correspondents_having_roles is None else [
            CorrespondentFacade(self.url_prefix, c.correspondent, self.with_relationships_links,
                                self.with_relationships_data).resource
            for c in self.obj.correspondents_having_roles
        ]

    @property
    def resource(self):
        resource = {
            **self.resource_identifier,
            "attributes": {
                "title": self.obj.title,
                "witness-label": self.obj.witness_label,
                "classification-mark": self.obj.classification_mark,
                "argument": self.obj.argument,
                "creation": self.obj.creation,
                "creation-label": self.obj.creation_label,
                "location-date-label": self.obj.location_date_label,
                "location-date-ref": self.obj.location_date_ref,
                "transcription": self.obj.transcription,
                "date-insert": self.obj.date_insert,
                "date-update": self.obj.date_update,
                "is-published": self.obj.is_published,
            },
            "meta": self.meta,
            "links": {
                "self": self.self_link
            }
        }
        if self.with_relationships_links:
            resource["relationships"] = self.get_exposed_relationships()
        return resource

    def __init__(self, *args, **kwargs):
        super(DocumentFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is a document
        """

        self.relationships = {
            "correspondents-having-roles": {
                "links": self._get_links(rel_name="correspondents-having-roles"),
                "resource_identifier_getter": self.get_correspondents_having_roles_resource_identifiers,
                "resource_getter": self.get_correspondents_having_roles_resources
            },
            "roles": {
                "links": self._get_links(rel_name="roles"),
                "resource_identifier_getter": self.get_role_resource_identifiers,
                "resource_getter": self.get_role_resources
            },
            "correspondents": {
                "links": self._get_links(rel_name="correspondents"),
                "resource_identifier_getter": self.get_correspondent_resource_identifiers,
                "resource_getter": self.get_correspondent_resources
            },
        }

        # ===================================
        # Add simple relationships
        # ===================================
        from app.api.image.facade import ImageFacade
        from app.api.note.facade import NoteFacade
        from app.api.language.facade import LanguageFacade
        from app.api.institution.facade import InstitutionFacade
        from app.api.tradition.facade import TraditionFacade
        from app.api.user.facade import UserFacade
        from app.api.whitelist.facade import WhitelistFacade
        from app.api.collection.facade import CollectionFacade

        for rel_name, (rel_facade, to_many) in {
            "collections": (CollectionFacade, True),
            "images": (ImageFacade, True),
            "notes": (NoteFacade, True),
            "languages": (LanguageFacade, True),
            "institution": (InstitutionFacade, False),
            "tradition": (TraditionFacade, False),
            "owner": (UserFacade, False),
            "whitelist": (WhitelistFacade, False),
            "prev-document": (DocumentFacade, False),
            "next-document": (DocumentFacade, False)
        }.items():
            u_rel_name = rel_name.replace("-", "_")

            self.relationships[rel_name] = {
                "links": self._get_links(rel_name=rel_name),
                "resource_identifier_getter": self.get_related_resource_identifiers(rel_facade, u_rel_name, to_many),
                "resource_getter": self.get_related_resources(rel_facade, u_rel_name, to_many),
            }

    @property
    def indexed_data(self):
        return {
            "id": self.resource["id"],
            "type": self.resource["type"],

            "title": self.resource["attributes"]["title"],
            "argument": self.resource["attributes"]["argument"],
            "transcription": self.resource["attributes"]["transcription"],

            "manifest-url": None if len(self.obj.images) == 0 else self.obj.images[0].manifest_url,
            "languages": None if len(self.obj.languages) == 0 else ";".join([l.code for l in self.obj.languages]),
            "collections": None if len(self.obj.collections) == 0 else ";".join([c.title for c in self.obj.collections]),
            "institution": self.obj.institution,
            "tradition": self.obj.tradition,
        }