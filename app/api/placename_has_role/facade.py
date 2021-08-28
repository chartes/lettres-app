
from app.api.abstract_facade import JSONAPIAbstractFacade
from app.models import PlacenameHasRole


class PlacenameHasRoleFacade(JSONAPIAbstractFacade):
    """

    """
    TYPE = "placename-has-role"
    TYPE_PLURAL = "placenames-having-roles"

    MODEL = PlacenameHasRole

    @property
    def id(self):
        return self.obj.id

    @property
    def resource(self):
        resource = {
            **self.resource_identifier,
            "attributes": {
                "function": self.obj.function,
                "field": self.obj.field
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
        super(PlacenameHasRoleFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is the relation between a placename and its role within a document
        """
        # ===================================
        # Add simple relationships
        # ===================================
        from app.api.document.facade import DocumentFacade
        from app.api.placename.facade import PlacenameFacade
        from app.api.placename_role.facade import PlacenameRoleFacade

        for rel_name, (rel_facade, to_many) in {
            "placename-role": (PlacenameRoleFacade, False),
            "document": (DocumentFacade, False),
            "placename": (PlacenameFacade, False),
        }.items():
            u_rel_name = rel_name.replace("-", "_")

            self.relationships[rel_name] = {
                "links": self._get_links(rel_name=rel_name),
                "resource_identifier_getter": self.get_related_resource_identifiers(rel_facade, u_rel_name, to_many),
                "resource_getter": self.get_related_resources(rel_facade, u_rel_name, to_many),
            }

    def get_data_to_index_when_added(self, propagate):
        return self.get_relationship_data_to_index(rel_name="placename")


class PlacenameHasRoleIncludedFacade(PlacenameHasRoleFacade):
    def __init__(self, *args, **kwargs):
        super(PlacenameHasRoleIncludedFacade, self).__init__(*args, **kwargs)

    @property
    def resource(self):
        print('======'*100)
        resource = {
            **self.resource_identifier,
            "attributes": {
                "function": self.obj.function,
                "field": self.obj.field,
                "placename_id": self.obj.placename_id,
                "document_id": self.obj.document_id,
                "role_id": self.obj.placename_role_id
            },
            "meta": self.meta,
            "links": {
                "self": self.self_link
            }
        }

        return resource
