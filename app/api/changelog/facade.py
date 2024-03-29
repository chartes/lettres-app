from app.api.abstract_facade import JSONAPIAbstractFacade
from app.models import Changelog, datetime_to_str


class ChangelogFacade(JSONAPIAbstractFacade):
    """

    """
    TYPE = "change"
    TYPE_PLURAL = "changes"

    MODEL = Changelog

    @property
    def id(self):
        return self.obj.id

    @property
    def resource(self):
        resource = {
            **self.resource_identifier,
            "attributes": {
                "object-id": self.obj.object_id,
                "object-type": self.obj.object_type,

                "event-date": datetime_to_str(self.obj.event_date),
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
        super(ChangelogFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is a change in the changelog
        """
        from app.api.user.facade import UserFacade

        self.relationships = {
            "user": {
                "links": self._get_links(rel_name="user"),
                "resource_identifier_getter": self.get_related_resource_identifiers(UserFacade, "user"),
                "resource_getter": self.get_related_resources(UserFacade, "user"),
            }
        }
