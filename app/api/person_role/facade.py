
from app.api.abstract_facade import JSONAPIAbstractFacade
from app.models import PersonRole


class PersonRoleFacade(JSONAPIAbstractFacade):
    """

    """
    TYPE = "person-role"
    TYPE_PLURAL = "person-roles"

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def get_resource_facade(url_prefix, id, **kwargs):
        e = PersonRole.query.filter(PersonRole.id == id).first()
        if e is None:
            kwargs = {"status": 404}
            errors = [{"status": 404, "title": "person role %s does not exist" % id}]
        else:
            e = PersonRoleFacade(url_prefix, e, **kwargs)
            kwargs = {}
            errors = []
        return e, kwargs, errors

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

