from app import db
from app.api.abstract_facade import JSONAPIAbstractFacade
from app.models import Note


class NoteFacade(JSONAPIAbstractFacade):
    """

    """
    TYPE = "note"
    TYPE_PLURAL = "notes"

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def get_resource_facade(url_prefix, id, **kwargs):
        e = Note.query.filter(Note.id == id).first()
        if e is None:
            kwargs = {"status": 404}
            errors = [{"status": 404, "title": "note %s does not exist" % id}]
        else:
            e = NoteFacade(url_prefix, e, **kwargs)
            kwargs = {}
            errors = []
        return e, kwargs, errors

    def get_document_resource_identifier(self):
        from app.api.document.facade import DocumentFacade
        return None if self.obj.document is None else DocumentFacade.make_resource_identifier(
            self.obj.document.id, DocumentFacade.TYPE
        )

    def get_document_resource(self):
        from app.api.document.facade import DocumentFacade
        return None if self.obj.document is None else DocumentFacade(
            self.url_prefix, self.obj.document, self.with_relationships_links, self.with_relationships_data
        ).resource

    def __init__(self, *args, **kwargs):
        super(NoteFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is an note
        """

        self.relationships = {
            "document": {
                "links": self._get_links(rel_name="document"),
                "resource_identifier_getter": self.get_document_resource_identifier,
                "resource_getter": self.get_document_resource
            },
        }
        self.resource = {
            **self.resource_identifier,
            "attributes": {
                "label": self.obj.label,
                "content": self.obj.content,
            },
            "meta": self.meta,
            "links": {
                "self": self.self_link
            }
        }

        if self.with_relationships_links:
            self.resource["relationships"] = self.get_exposed_relationships()
