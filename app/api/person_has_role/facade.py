
from app.api.abstract_facade import JSONAPIAbstractFacade
from app.models import PersonHasRole


class PersonHasRoleFacade(JSONAPIAbstractFacade):
    """

    """
    TYPE = "person-has-role"
    TYPE_PLURAL = "persons-having-roles"

    MODEL = PersonHasRole

    @property
    def id(self):
        return self.obj.id

    @property
    def resource(self):
        resource = {
            **self.resource_identifier,
            "attributes": {
                "function": self.obj.function
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
        super(PersonHasRoleFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is the relation between a person and its role within a document
        """
        # ===================================
        # Add simple relationships
        # ===================================
        from app.api.document.facade import DocumentFacade
        from app.api.person.facade import PersonFacade
        from app.api.person_role.facade import PersonRoleFacade

        for rel_name, (rel_facade, to_many) in {
            "person-role": (PersonRoleFacade, False),
            "document": (DocumentFacade, False),
            "person": (PersonFacade, False),
        }.items():
            u_rel_name = rel_name.replace("-", "_")

            self.relationships[rel_name] = {
                "links": self._get_links(rel_name=rel_name),
                "resource_identifier_getter": self.get_related_resource_identifiers(rel_facade, u_rel_name, to_many),
                "resource_getter": self.get_related_resources(rel_facade, u_rel_name, to_many),
            }

