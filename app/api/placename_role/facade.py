
from app.api.abstract_facade import JSONAPIAbstractFacade
from app.models import PlacenameRole


class PlacenameRoleFacade(JSONAPIAbstractFacade):
    """

    """
    TYPE = "placename-role"
    TYPE_PLURAL = "placename-roles"

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def get_resource_facade(url_prefix, id, **kwargs):
        e = PlacenameRole.query.filter(PlacenameRole.id == id).first()
        if e is None:
            kwargs = {"status": 404}
            errors = [{"status": 404, "title": "placename role %s does not exist" % id}]
        else:
            e = PlacenameRoleFacade(url_prefix, e, **kwargs)
            kwargs = {}
            errors = []
        return e, kwargs, errors

    @property
    def resource(self):
        resource = {
            **self.resource_identifier,
            "attributes": {
                "id": self.obj.id,
                "label": self.obj.label,
                "description": self.obj.description
            },
            "meta": self.meta,
            "links": {
                "self": self.self_link
            }
        }
        if self.with_relationships_links:
            resource["relationships"] = self.get_exposed_relationships()
        return resource

