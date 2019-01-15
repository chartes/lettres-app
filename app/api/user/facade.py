
from app.api.abstract_facade import JSONAPIAbstractFacade
from app.models import User


class UserFacade(JSONAPIAbstractFacade):
    """

    """
    TYPE = "user"
    TYPE_PLURAL = "users"

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def get_resource_facade(url_prefix, id, **kwargs):
        e = User.query.filter(User.id == id).first()
        if e is None:
            kwargs = {"status": 404}
            errors = [{"status": 404, "title": "user %s does not exist" % id}]
        else:
            e = UserFacade(url_prefix, e, **kwargs)
            kwargs = {}
            errors = []
        return e, kwargs, errors

    @staticmethod
    def create_resource(model, obj_id, attributes, related_resources):
        resource = None
        errors = [{"status": 403, "title": "You cannot create a 'User' from the API"}]
        return resource, errors

    @property
    def resource(self):
        resource = {
            **self.resource_identifier,
            "attributes": {
                "username": self.obj.username,
                "email": self.obj.email,
                "confirmed-at": self.obj.email_confirmed_at,
                "is-active": self.obj.active,
                "firstname": self.obj.first_name,
                "lastname": self.obj.last_name
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
        super(UserFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is a user 
        """
        from app.api.user_role.facade import UserRoleFacade
        from app.api.document.facade import DocumentFacade
        self.relationships = {
            "roles": {
                "links": self._get_links(rel_name="roles"),
                "resource_identifier_getter": self.get_related_resource_identifiers(UserRoleFacade, "roles", to_many=True),
                "resource_getter": self.get_related_resources(UserRoleFacade, "roles", to_many=True),
            },
            "owned-documents": {
                "links": self._get_links(rel_name="owned-documents"),
                "resource_identifier_getter": self.get_related_resource_identifiers(DocumentFacade, "owned_documents", to_many=True),
                "resource_getter": self.get_related_resources(DocumentFacade, "owned_documents", to_many=True),
            }
        }
