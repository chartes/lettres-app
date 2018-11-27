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

    # noinspection PyArgumentList
    @staticmethod
    def create_resource(id, attributes, related_resources):
        resource = None
        errors = None
        try:
            _g = attributes.get
            co = Image(
                id=id,
                img_url=_g("img-url"),
                manifest_url=_g("manifest-url"),
                document_id=_g("document-id"),
            )
            db.session.add(co)
            db.session.commit()
            resource = co
        except Exception as e:
            print(e)
            errors = [{"status": 403, "title": "Error creating resource 'Image' with data: %s" % (str([id, attributes, related_resources]))}]
            db.session.rollback()
        return resource, errors

    def __init__(self, *args, **kwargs):
        super(ImageFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is an image
        """

        self.relationships = {

        }
        self.resource = {
            **self.resource_identifier,
            "attributes": {
                "id": self.obj.id,
                "img-url": self.obj.img_url,
                "manifest-url": self.obj.manifest_url,
            },
            "meta": self.meta,
            "links": {
                "self": self.self_link
            }
        }

        if self.with_relationships_links:
            self.resource["relationships"] = self.get_exposed_relationships()
