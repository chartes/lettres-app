from app.api.abstract_facade import JSONAPIAbstractFacade
from app.models import Whitelist


class WhitelistFacade(JSONAPIAbstractFacade):
    """

    """
    TYPE = "whitelist"
    TYPE_PLURAL = "whitelists"

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def get_resource_facade(url_prefix, id, **kwargs):
        e = Whitelist.query.filter(Whitelist.id == id).first()
        if e is None:
            kwargs = {"status": 404}
            errors = [{"status": 404, "title": "whitelist %s does not exist" % id}]
        else:
            e = WhitelistFacade(url_prefix, e, **kwargs)
            kwargs = {}
            errors = []
        return e, kwargs, errors

    @property
    def resource(self):
        resource = {
            **self.resource_identifier,
            "attributes": {
                "label": self.obj.label,
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
        super(WhitelistFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is a whitelist
        """

        from app.api.user.facade import UserFacade
        from app.api.document.facade import DocumentFacade
        self.relationships = {
            "users": {
                "links": self._get_links(rel_name="users"),
                "resource_identifier_getter": self.get_related_resource_identifiers(UserFacade, "users", to_many=True),
                "resource_getter": self.get_related_resources(UserFacade, "users", to_many=True)
            },
            "owner": {
                "links": self._get_links(rel_name="owner"),
                "resource_identifier_getter": self.get_related_resource_identifiers(UserFacade, "owner"),
                "resource_getter": self.get_related_resources(UserFacade, "owner")
            },
            "documents": {
                "links": self._get_links(rel_name="documents"),
                "resource_identifier_getter": self.get_related_resource_identifiers(DocumentFacade, "documents", to_many=True),
                "resource_getter": self.get_related_resources(DocumentFacade, "documents", to_many=True),
            },
        }
