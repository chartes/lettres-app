from app import db
from app.api.abstract_facade import JSONAPIAbstractFacade
from app.models import Lock, datetime_to_str


class LockFacade(JSONAPIAbstractFacade):
    """

    """
    TYPE = "lock"
    TYPE_PLURAL = "locks"

    MODEL = Lock

    @property
    def id(self):
        return self.obj.id

    #@staticmethod
    #def get_resource_facade(url_prefix, id, **kwargs):
    #    e = Lock.query.filter(Lock.id == id).first()
    #    if e is None:
    #        kwargs = {"status": 404}
    #        errors = [{"status": 404, "title": "lock %s does not exist" % id}]
    #    else:
    #        e = LockFacade(url_prefix, e, **kwargs)
    #        kwargs = {}
    #        errors = []
    #    return e, kwargs, errors

    @property
    def resource(self):
        resource = {
            **self.resource_identifier,
            "attributes": {
                "object-id": self.obj.object_id,
                "object-type": self.obj.object_type,

                "event-date": datetime_to_str(self.obj.event_date),
                "expiration-date": datetime_to_str(self.obj.expiration_date),
                "is-active": self.obj.is_active,
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
        super(LockFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is a lock
        """
        from app.api.user.facade import UserFacade

        self.relationships = {
            "user": {
                "links": self._get_links(rel_name="user"),
                "resource_identifier_getter": self.get_related_resource_identifiers(UserFacade, "user"),
                "resource_getter": self.get_related_resources(UserFacade, "user"),
            }
        }
