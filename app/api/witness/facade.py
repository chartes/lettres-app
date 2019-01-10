from app import db
from app.api.abstract_facade import JSONAPIAbstractFacade
from app.models import Witness

class WitnessFacade(JSONAPIAbstractFacade):
    """

    """
    TYPE = "witness"
    TYPE_PLURAL = "witnesses"

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def get_resource_facade(url_prefix, id, **kwargs):
        e = Witness.query.filter(Witness.id == id).first()
        if e is None:
            kwargs = {"status": 404}
            errors = [{"status": 404, "title": "witness %s does not exist" % id}]
        else:
            e = WitnessFacade(url_prefix, e, **kwargs)
            kwargs = {}
            errors = []
        return e, kwargs, errors

    @property
    def resource(self):
        resource = {
            **self.resource_identifier,
            "attributes": {
                "content": self.obj.content,
                "tradition": self.obj.tradition,
                "status": self.obj.status,
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
        super(WitnessFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is a witness
        """

        from app.api.image.facade import ImageFacade
        from app.api.institution.facade import InstitutionFacade
        from app.api.document.facade import DocumentFacade

        self.relationships = {
            "document": {
                "links": self._get_links(rel_name="document"),
                "resource_identifier_getter": self.get_related_resource_identifiers(DocumentFacade, "document",
                                                                                    to_many=False),
                "resource_getter": self.get_related_resources(DocumentFacade, "document", to_many=False),
            },
            "institution": {
                "links": self._get_links(rel_name="institution"),
                "resource_identifier_getter": self.get_related_resource_identifiers(InstitutionFacade, "institution",
                                                                                    to_many=False),
                "resource_getter": self.get_related_resources(InstitutionFacade, "institution", to_many=False),
            },
            "images": {
                "links": self._get_links(rel_name="images"),
                "resource_identifier_getter":  self.get_related_resource_identifiers(ImageFacade, "images", to_many=True),
                "resource_getter":  self.get_related_resources(ImageFacade, "images", to_many=True),
            },
        }
