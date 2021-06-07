
from app.api.abstract_facade import JSONAPIAbstractChangeloggedFacade, JSONAPIAbstractFacade
from app.models import Placename


class PlacenameFacade(JSONAPIAbstractChangeloggedFacade):
    """

    """
    TYPE = "placename"
    TYPE_PLURAL = "placenames"

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def get_resource_facade(url_prefix, id, **kwargs):
        e = Placename.query.filter(Placename.id == id).first()
        if e is None:
            kwargs = {"status": 404}
            errors = [{"status": 404, "title": "placename %s does not exist" % id}]
        else:
            e = PlacenameFacade(url_prefix, e, **kwargs)
            kwargs = {}
            errors = []
        return e, kwargs, errors

    @staticmethod
    def update_resource(obj, obj_type, attributes, related_resources, append=False):
        # rename the relationship
        if "roles-within-documents" in related_resources:
            related_resources["placenames_having_roles"] = related_resources.pop("roles-within-documents")
        return JSONAPIAbstractFacade.update_resource(obj, obj_type, attributes, related_resources, append)

    def get_document_resource_identifiers(self, rel_facade=None):
        from app.api.document.facade import DocumentFacade
        rel_facade = DocumentFacade if not rel_facade else rel_facade

        return [] if self.obj.placenames_having_roles is None else [
            rel_facade.make_resource_identifier(c_h_r.document.id, rel_facade.TYPE)
            for c_h_r in self.obj.placenames_having_roles
        ]

    def get_document_resources(self, rel_facade=None):
        from app.api.document.facade import DocumentFacade
        rel_facade = DocumentFacade if not rel_facade else rel_facade

        return [] if self.obj.placenames_having_roles is None else [
            rel_facade(self.url_prefix, c.document, self.with_relationships_links,
                           self.with_relationships_data).resource
            for c in self.obj.placenames_having_roles
        ]

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
                "links": self._get_links(rel_name="roles-within-documents"),
                "resource_identifier_getter": self.get_roles_resource_identifiers,
                "resource_getter": self.get_roles_resources
            },
            "documents": {
                "links": self._get_links(rel_name="documents"),
                "resource_identifier_getter": self.get_document_resource_identifiers,
                "resource_getter": self.get_document_resources
            },
        })

    def get_data_to_index_when_added(self, propagate):
        _res = self.resource
        payload = {
            "id": _res["id"],
            "type": _res["type"],
            "label": _res["attributes"]["label"]
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
