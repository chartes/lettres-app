
from app.api.abstract_facade import JSONAPIAbstractChangeloggedFacade
from app.models import CorrespondentHasRole


class CorrespondentHasRoleFacade(JSONAPIAbstractChangeloggedFacade):
    """

    """
    TYPE = "correspondent-has-role"
    TYPE_PLURAL = "correspondents-having-roles"

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def get_resource_facade(url_prefix, id, **kwargs):
        e = CorrespondentHasRole.query.filter(CorrespondentHasRole.id == id).first()
        if e is None:
            kwargs = {"status": 404}
            errors = [{"status": 404, "title": "CorrespondentHasRole %s does not exist" % id}]
        else:
            e = CorrespondentHasRoleFacade(url_prefix, e, **kwargs)
            kwargs = {}
            errors = []
        return e, kwargs, errors

    @property
    def resource(self):
        resource = {
            **self.resource_identifier,
            "attributes": {
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
        super(CorrespondentHasRoleFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is the relation between a correspondent and its role within a document
        """
        # ===================================
        # Add simple relationships
        # ===================================
        from app.api.document.facade import DocumentFacade
        from app.api.correspondent.facade import CorrespondentFacade
        from app.api.correspondent_role.facade import CorrespondentRoleFacade

        for rel_name, (rel_facade, to_many) in {
            "correspondent-role": (CorrespondentRoleFacade, False),
            "document": (DocumentFacade, False),
            "correspondent": (CorrespondentFacade, False),
        }.items():
            u_rel_name = rel_name.replace("-", "_")

            self.relationships[rel_name] = {
                "links": self._get_links(rel_name=rel_name),
                "resource_identifier_getter": self.get_related_resource_identifiers(rel_facade, u_rel_name, to_many),
                "resource_getter": self.get_related_resources(rel_facade, u_rel_name, to_many),
            }

