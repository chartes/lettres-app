
from app.api.abstract_facade import JSONAPIAbstractFacade
from app.models import User, datetime_to_str


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
                "confirmed-at": datetime_to_str(self.obj.email_confirmed_at),
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
        from app.api.lock.facade import LockFacade
        from app.api.document.facade import DocumentFacade

        self.relationships = {
            "roles": {
                "links": self._get_links(rel_name="roles"),
                "resource_identifier_getter": self.get_related_resource_identifiers(UserRoleFacade, "roles", to_many=True),
                "resource_getter": self.get_related_resources(UserRoleFacade, "roles", to_many=True),
            },

            "locks": {
                "links": self._get_links(rel_name="locks"),
                "resource_identifier_getter": self.get_related_resource_identifiers(LockFacade, "locks",
                                                                                    to_many=True),
                "resource_getter": self.get_related_resources(LockFacade, "locks", to_many=True),
            },

            "bookmarks": {
                "links": self._get_links(rel_name="bookmarks"),
                "resource_identifier_getter": self.get_related_resource_identifiers(DocumentFacade, "bookmarks",
                                                                                    to_many=True),
                "resource_getter": self.get_related_resources(DocumentFacade, "bookmarks", to_many=True),
            }
        }

    def get_data_to_index_when_added(self, propagate):
        _res = self.resource
        payload = {
            "id": _res["id"],
            "type": _res["type"],

            "username": _res["attributes"]["username"],
            "firstname": _res["attributes"]["firstname"],
            "lastname": _res["attributes"]["lastname"],
        }
        return [{"id": _res["id"], "index": self.get_index_name(), "payload": payload}]

    def remove_from_index(self, propagate):
        from app.search import SearchIndexManager
        SearchIndexManager.remove_from_index(index=self.get_index_name(), id=self.id)