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

    @property
    def resource(self):
        resource = {
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
            resource["relationships"] = self.get_exposed_relationships()

        return resource

    def __init__(self, *args, **kwargs):
        super(NoteFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is an note
        """

        from app.api.document.facade import DocumentFacade
        self.relationships = {
            "document": {
                "links": self._get_links(rel_name="document"),
                "resource_identifier_getter": self.get_related_resource_identifiers(DocumentFacade, "document"),
                "resource_getter": self.get_related_resources(DocumentFacade, "document"),
            },
        }
