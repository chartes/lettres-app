from app import db
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

    def get_role_resource_identifier(self):
        from app.api.user_role.facade import UserRoleFacade
        return None if self.obj.role is None else UserRoleFacade.make_resource_identifier(
            self.obj.role.id,
            UserRoleFacade.TYPE
        )

    def get_role_resource(self):
        from app.api.user_role.facade import UserRoleFacade
        return None if self.obj.role is None else UserRoleFacade(self.url_prefix,
                                                                 self.obj.role,
                                                                 self.with_relationships_links,
                                                                 self.with_relationships_data).resource

    def get_owned_document_resource_identifiers(self):
        from app.api.document.facade import DocumentFacade
        return [] if self.obj.owned_documents is None else [
            DocumentFacade.make_resource_identifier(c.id, DocumentFacade.TYPE)
            for c in self.obj.owned_documents
        ]

    def get_owned_document_having_roles_resources(self):
        from app.api.document.facade import DocumentFacade
        return [] if self.obj.owned_documents is None else [
            DocumentFacade(self.url_prefix, c, self.with_relationships_links, self.with_relationships_data).resource
            for c in self.obj.owned_documents
        ]

    @staticmethod
    def create_resource(id, attributes, related_resources):
        resource = None
        errors = [{"status": 403, "title": "You cannot create a 'User' from the API"}]
        return resource, errors

    def __init__(self, *args, **kwargs):
        super(UserFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is a user 
        """

        self.relationships = {
            "role": {
                "links": self._get_links(rel_name="role"),
                "resource_identifier_getter": self.get_role_resource_identifier,
                "resource_getter": self.get_role_resource,
                "resource_attribute": "role"
            },
            "owned-documents": {
                "links": self._get_links(rel_name="owned-documents"),
                "resource_identifier_getter": self.get_owned_document_resource_identifiers,
                "resource_getter": self.get_owned_document_having_roles_resources,
                "resource_attribute": "owned_documents"
            }
        }
        self.resource = {
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
            self.resource["relationships"] = self.get_exposed_relationships()
