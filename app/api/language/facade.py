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

        from app.api.document.facade import DocumentFacade
        self.relationships = {
            "documents": {
                "links": self._get_links(rel_name="documents"),
                "resource_identifier_getter": self.get_related_resource_identifiers(DocumentFacade, "documents", to_many=True),
                "resource_getter": self.get_related_resources(DocumentFacade, "documents", to_many=True),
            },
        }
