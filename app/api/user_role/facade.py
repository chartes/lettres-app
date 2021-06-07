from app.api.abstract_facade import JSONAPIAbstractFacade
from app.models import UserRole


class UserRoleFacade(JSONAPIAbstractFacade):
    """

    """
    TYPE = "user_role"
    TYPE_PLURAL = "user-roles"

    MODEL = UserRole

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def create_resource(model, obj_id, attributes, related_resources):
        resource = None
        errors = [{"status": 403, "title": "You cannot create a 'User Role' from the API"}]
        return resource, errors

    @property
    def resource(self):
        resource = {
            **self.resource_identifier,
            "attributes": {
                "name": self.obj.name,
                "description": self.obj.description,
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
        super(UserRoleFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is a user role
        """

        self.relationships = {
        }
