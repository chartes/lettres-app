
from app.api.abstract_facade import JSONAPIAbstractFacade
from app.models import Correspondent


class CorrespondentFacade(JSONAPIAbstractFacade):
    """

    """
    TYPE = "correspondent"
    TYPE_PLURAL = "correspondents"

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def get_resource_facade(url_prefix, id, **kwargs):
        e = Correspondent.query.filter(Correspondent.id == id).first()
        if e is None:
            kwargs = {"status": 404}
            errors = [{"status": 404, "title": "correspondent %s does not exist" % id}]
        else:
            e = CorrespondentFacade(url_prefix, e, **kwargs)
            kwargs = {}
            errors = []
        return e, kwargs, errors

    def get_document_resource_identifiers(self):
        from app.api.document.facade import DocumentFacade
        return [] if self.obj.correspondents_having_roles is None else [
            DocumentFacade.make_resource_identifier(c_h_r.document.id, DocumentFacade.TYPE)
            for c_h_r in self.obj.correspondents_having_roles
        ]

    def get_document_resources(self):
        from app.api.document.facade import DocumentFacade
        return [] if self.obj.correspondents_having_roles is None else [
            DocumentFacade(self.url_prefix, c.document, self.with_relationships_links,
                           self.with_relationships_data).resource
            for c in self.obj.correspondents_having_roles
        ]

    def get_roles_resource_identifiers(self):
        from app.api.correspondent_has_role.facade import CorrespondentHasRoleFacade
        return [] if self.obj.correspondents_having_roles is None else [
            CorrespondentHasRoleFacade.make_resource_identifier(e.id, CorrespondentHasRoleFacade.TYPE)
            for e in self.obj.correspondents_having_roles]

    def get_roles_resources(self):
        from app.api.correspondent_has_role.facade import CorrespondentHasRoleFacade
        return [] if self.obj.correspondents_having_roles is None else [CorrespondentHasRoleFacade(self.url_prefix, e,
                                                                                                   self.with_relationships_links,
                                                                                                   self.with_relationships_data).resource
                                                                        for e in self.obj.correspondents_having_roles]

    def __init__(self, *args, **kwargs):
        super(CorrespondentFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is a correspondent
        """

        self.relationships = {
            "roles-within-documents": {
                "links": self._get_links(rel_name="roles-within-documents"),
                "resource_identifier_getter": self.get_roles_resource_identifiers,
                "resource_getter": self.get_roles_resources
            },
            "documents": {
                "links": self._get_links(rel_name="documents"),
                "resource_identifier_getter": self.get_document_resource_identifiers,
                "resource_getter": self.get_document_resources
            },
        }
        self.resource = {
            **self.resource_identifier,
            "attributes": {
                "firstname": self.obj.firstname,
                "lastname": self.obj.lastname,
                "key": self.obj.key,
                "ref": self.obj.ref,
            },
            "meta": self.meta,
            "links": {
                "self": self.self_link
            }
        }

        if self.with_relationships_links:
            self.resource["relationships"] = self.get_exposed_relationships()
