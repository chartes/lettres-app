
from app.api.abstract_facade import JSONAPIAbstractFacade
from app.models import PlacenameRole


class PlacenameRoleFacade(JSONAPIAbstractFacade):
    """

    """
    TYPE = "placename-role"
    TYPE_PLURAL = "placename-roles"

    MODEL = PlacenameRole

    @property
    def id(self):
        return self.obj.id

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

