from app import db
from app.api.abstract_facade import JSONAPIAbstractFacade
from app.models import Image


class ImageFacade(JSONAPIAbstractFacade):
    """

    """
    TYPE = "image"
    TYPE_PLURAL = "images"

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def get_resource_facade(url_prefix, id, **kwargs):
        e = Image.query.filter(Image.id == id).first()
        if e is None:
            kwargs = {"status": 404}
            errors = [{"status": 404, "title": "image %s does not exist" % id}]
        else:
            e = ImageFacade(url_prefix, e, **kwargs)
            kwargs = {}
            errors = []
        return e, kwargs, errors

    @property
    def resource(self):
        resource = {
            **self.resource_identifier,
            "attributes": {
                "canvas-id": self.obj.canvas_id,
                "order-num": self.obj.order_num,
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
        super(ImageFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is an image
        """

        from app.api.witness.facade import WitnessFacade
        self.relationships = {
            "witness": {
                "links": self._get_links(rel_name="witness"),
                "resource_identifier_getter": self.get_related_resource_identifiers(WitnessFacade, "witness"),
                "resource_getter": self.get_related_resources(WitnessFacade, "witness"),
            },
        }
