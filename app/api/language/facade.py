from app import db
from app.api.abstract_facade import JSONAPIAbstractFacade
from app.models import Language


class LanguageFacade(JSONAPIAbstractFacade):
    """

    """
    TYPE = "language"
    TYPE_PLURAL = "languages"

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def get_resource_facade(url_prefix, id, **kwargs):
        e = Language.query.filter(Language.id == id).first()
        if e is None:
            kwargs = {"status": 404}
            errors = [{"status": 404, "title": "language %s does not exist" % id}]
        else:
            e = LanguageFacade(url_prefix, e, **kwargs)
            kwargs = {}
            errors = []
        return e, kwargs, errors

    def get_document_resource_identifiers(self):
        from app.api.document.facade import DocumentFacade
        return [] if self.obj.documents is None else [
            DocumentFacade.make_resource_identifier(c.id, DocumentFacade.TYPE)
            for c in self.obj.documents
        ]

    def get_document_resources(self):
        from app.api.document.facade import DocumentFacade
        return [] if self.obj.documents is None else [
            DocumentFacade(self.url_prefix, c, self.with_relationships_links, self.with_relationships_data).resource
            for c in self.obj.documents
        ]

    @property
    def resource(self):
        resource = {
            **self.resource_identifier,
            "attributes": {
                "code": self.obj.code,
                "label": self.obj.label
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
        super(LanguageFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is a language
        """

        self.relationships = {
            "documents": {
                "links": self._get_links(rel_name="documents"),
                "resource_identifier_getter": self.get_document_resource_identifiers,
                "resource_getter": self.get_document_resources,
                "resource_attribute": "documents"
            },
        }
