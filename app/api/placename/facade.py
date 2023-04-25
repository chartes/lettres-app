
from app.api.abstract_facade import JSONAPIAbstractChangeloggedFacade, JSONAPIAbstractFacade
from app.models import Placename


class PlacenameFacade(JSONAPIAbstractChangeloggedFacade):
    """

    """
    TYPE = "placename"
    TYPE_PLURAL = "placenames"

    MODEL = Placename

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def update_resource(obj, obj_type, attributes, related_resources, append=False):
        # rename the relationship
        if "roles-within-documents" in related_resources:
            related_resources["placenames_having_roles"] = related_resources.pop("roles-within-documents")
        return JSONAPIAbstractFacade.update_resource(obj, obj_type, attributes, related_resources, append)

    def get_document_resource_identifiers(self, rel_facade=None):
        from app.api.document.facade import DocumentFacade
        rel_facade = DocumentFacade if not rel_facade else rel_facade

        resIds = [] if self.obj.placenames_having_roles is None else [
            rel_facade.make_resource_identifier(c_h_r.document.id, rel_facade.TYPE)
            for c_h_r in self.obj.placenames_having_roles
        ]
        return list({object_['id']: object_ for object_ in resIds}.values())

    def get_document_resources(self, rel_facade=None):
        from app.api.document.facade import DocumentFacade
        rel_facade = DocumentFacade if not rel_facade else rel_facade

        resources = [] if self.obj.placenames_having_roles is None else [
            rel_facade(self.url_prefix, c.document, self.with_relationships_links,
                           self.with_relationships_data).resource
            for c in self.obj.placenames_having_roles
        ]
        return list({object_.id: object_ for object_ in resources}.values())

    def get_roles_resource_identifiers(self, rel_facade=None):
        from app.api.placename_has_role.facade import PlacenameHasRoleFacade
        rel_facade = PlacenameHasRoleFacade if not rel_facade else rel_facade

        return [] if self.obj.placenames_having_roles is None else [
            rel_facade.make_resource_identifier(e.id, rel_facade.TYPE)
            for e in self.obj.placenames_having_roles]

    def get_roles_resources(self, rel_facade=None):
        from app.api.placename_has_role.facade import PlacenameHasRoleFacade
        rel_facade = PlacenameHasRoleFacade if not rel_facade else rel_facade

        return [] if self.obj.placenames_having_roles is None else [rel_facade(self.url_prefix, e,
                                                                                     self.with_relationships_links,
                                                                                     self.with_relationships_data).resource
                                                                 for e in self.obj.placenames_having_roles]

    @property
    def resource(self):
        resource = {
            **self.resource_identifier,
            # TODO add label to ressource ? "label": self.obj.label,
            "attributes": {
                "label": self.obj.label,
                "long": self.obj.long,
                "lat": self.obj.lat,
                "ref": self.obj.ref,
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
        super(PlacenameFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is a placename
        """
        self.relationships.update({
            "roles-within-documents": {
                "links": self._get_links(rel_name="roles-within-documents"),  # TODO wrong ?
                "resource_identifier_getter": self.get_roles_resource_identifiers,
                "resource_getter": self.get_roles_resources
            },
            "documents": {
                "links": self._get_links(rel_name="documents"),  # TODO wrong ?
                "resource_identifier_getter": self.get_document_resource_identifiers,
                "resource_getter": self.get_document_resources
            }
        })

    def get_data_to_index_when_added(self, propagate):
        _res = self.resource

        from app.api.placename_has_role.facade import PlacenameHasRoleFacade

        rels = []
        for e in self.obj.placenames_having_roles:
            r = PlacenameHasRoleFacade(self.url_prefix, e, True, True).resource
            rels.append({
                "type": r["type"],
                "id": r["id"],
                "placename_function": r["attributes"]["function"],
                "placename_field": r["attributes"]["field"],
                "role_id": e.placename_role.id,
                "document_id": e.document.id
            })

        payload = {
            "id": _res["id"],
            "type": _res["type"],
            **_res["attributes"],

            "relationships":  rels
        }
        placename_data = [{"id": _res["id"], "index": self.get_index_name(), "payload": payload}]
        if not propagate:
            return placename_data
        else:
            return placename_data + self.get_relationship_data_to_index(rel_name="documents") + self.get_relationship_data_to_index(
                rel_name="roles-within-documents")

    def remove_from_index(self, propagate):
        from app.api.search import SearchIndexManager
        SearchIndexManager.remove_from_index(index=self.get_index_name(), id=self.id)

        if propagate:
            # reindex the docs without the resource
            for data in self.get_data_to_index_when_added(propagate):
                if data["payload"]["id"] != self.id and data["payload"]["type"] != self.TYPE:
                    data["payload"]["placenames"] = [l for l in data["payload"]["placenames"] if l.get("id") != self.id]
                    SearchIndexManager.add_to_index(index=data["index"], id=data["id"], payload=data["payload"])
