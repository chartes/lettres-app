from app import db
from app.api.abstract_facade import JSONAPIAbstractFacade
from app.models import Changelog, datetime_to_str


class ChangelogFacade(JSONAPIAbstractFacade):
    """

    """
    TYPE = "changelog"
    TYPE_PLURAL = "changelogs"

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def get_resource_facade(url_prefix, id, **kwargs):
        e = Changelog.query.filter(Changelog.id == id).first()
        if e is None:
            kwargs = {"status": 404}
            errors = [{"status": 404, "title": "changelog %s does not exist" % id}]
        else:
            e = ChangelogFacade(url_prefix, e, **kwargs)
            kwargs = {}
            errors = []
        return e, kwargs, errors

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
        """Make a JSONAPI resource object describing what is a changelog
        """
        self.relationships = {

        }
