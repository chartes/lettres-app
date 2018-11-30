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
                "img-url": self.obj.img_url,
                "manifest-url": self.obj.manifest_url,
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

        from app.api.document.facade import DocumentFacade
        self.relationships = {
            "document": {
                "links": self._get_links(rel_name="document"),
                "resource_identifier_getter": self.get_related_resource_identifiers(DocumentFacade, "document"),
                "resource_getter": self.get_related_resources(DocumentFacade, "document"),
            },
        }
