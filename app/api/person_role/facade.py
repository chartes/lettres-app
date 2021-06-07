
from app.api.abstract_facade import JSONAPIAbstractFacade
from app.models import PersonRole


class PersonRoleFacade(JSONAPIAbstractFacade):
    """

    """
    TYPE = "person-role"
    TYPE_PLURAL = "person-roles"

    MODEL = PersonRole

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

