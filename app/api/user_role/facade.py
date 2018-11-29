from app import db
from app.api.abstract_facade import JSONAPIAbstractFacade
from app.models import User


class UserRoleFacade(JSONAPIAbstractFacade):
    """

    """
    TYPE = "user_role"
    TYPE_PLURAL = "user-roles"

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def get_resource_facade(url_prefix, id, **kwargs):
        e = User.query.filter(User.id == id).first()
        if e is None:
            kwargs = {"status": 404}
            errors = [{"status": 404, "title": "user role %s does not exist" % id}]
        else:
            e = UserRoleFacade(url_prefix, e, **kwargs)
            kwargs = {}
            errors = []
        return e, kwargs, errors

    def get_user_resource_identifiers(self):
        from app.api.user.facade import UserFacade
        return [] if self.obj.users is None else [
            UserFacade.make_resource_identifier(c.id, UserFacade.TYPE)
            for c in self.obj.users
        ]

    def get_users_resources(self):
        from app.api.user.facade import UserFacade
        return [] if self.obj.users is None else [
            UserFacade(self.url_prefix, c, self.with_relationships_links, self.with_relationships_data).resource
            for c in self.obj.users
        ]

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
                "label": self.obj.label,
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
            "users": {
                "links": self._get_links(rel_name="users"),
                "resource_identifier_getter": self.get_user_resource_identifiers,
                "resource_getter": self.get_users_resources
            }
        }
