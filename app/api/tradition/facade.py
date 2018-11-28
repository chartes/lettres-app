from app import db
from app.api.abstract_facade import JSONAPIAbstractFacade
from app.models import Tradition


class TraditionFacade(JSONAPIAbstractFacade):
    """

    """

    TYPE = "tradition"
    TYPE_PLURAL = "traditions"

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def get_resource_facade(url_prefix, id, **kwargs):
        e = Tradition.query.filter(Tradition.id == id).first()
        if e is None:
            kwargs = {"status": 404}
            errors = [{"status": 404, "title": "tradition %s does not exist" % id}]
        else:
            e = TraditionFacade(url_prefix, e, **kwargs)
            kwargs = {}
            errors = []
        return e, kwargs, errors

    # noinspection PyArgumentList
    @staticmethod
    def create_resource(id, attributes, related_resources):
        resource = None
        errors = None
        try:
            _g = attributes.get
            co = Tradition(
                id=id,
                label=_g("label"),
                description=_g("description"),
            )
            db.session.add(co)
            db.session.commit()
            resource = co
        except Exception as e:
            print(e)
            errors = {
                "status": 403,
                "title": "Error creating resource 'Tradition' with data: %s" % str([id, attributes, related_resources]),
                "detail": str(e)
            }
            db.session.rollback()
        return resource, errors

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

    def __init__(self, *args, **kwargs):
        super(TraditionFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is a tradition

        """

        self.relationships = {
            "documents": {
                "links": self._get_links(rel_name="documents"),
                "resource_identifier_getter": self.get_document_resource_identifiers,
                "resource_getter": self.get_document_resources,
                "resource_attribute": "documents"
            },
        }
        self.resource = {
            **self.resource_identifier,
            "attributes": {
                "label": self.obj.label,
                "description": self.obj.description
            },
            "meta": self.meta,
            "links": {
                "self": self.self_link
            }
        }

        if self.with_relationships_links:
            self.resource["relationships"] = self.get_exposed_relationships()
