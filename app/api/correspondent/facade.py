
from app.api.abstract_facade import JSONAPIAbstractChangeloggedFacade, JSONAPIAbstractFacade
from app.models import Correspondent


class CorrespondentFacade(JSONAPIAbstractChangeloggedFacade):
    """

    """
    TYPE = "correspondent"
    TYPE_PLURAL = "correspondents"

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def get_resource_facade(url_prefix, id, **kwargs):
        e = Correspondent.query.filter(Correspondent.id == id).first()
        if e is None:
            kwargs = {"status": 404}
            errors = [{"status": 404, "title": "correspondent %s does not exist" % id}]
        else:
            e = CorrespondentFacade(url_prefix, e, **kwargs)
            kwargs = {}
            errors = []
        return e, kwargs, errors

    @staticmethod
    def update_resource(obj, obj_type, attributes, related_resources, append=False):
        # rename the relationship
        if "roles-within-documents" in related_resources:
            related_resources["correspondents_having_roles"] = related_resources.pop("roles-within-documents")
        return JSONAPIAbstractFacade.update_resource(obj, obj_type, attributes, related_resources, append)

    def get_document_resource_identifiers(self):
        from app.api.document.facade import DocumentFacade
        return [] if self.obj.correspondents_having_roles is None else [
            DocumentFacade.make_resource_identifier(c_h_r.document.id, DocumentFacade.TYPE)
            for c_h_r in self.obj.correspondents_having_roles
        ]

    def get_document_resources(self):
        from app.api.document.facade import DocumentFacade
        return [] if self.obj.correspondents_having_roles is None else [
            DocumentFacade(self.url_prefix, c.document, self.with_relationships_links,
                           self.with_relationships_data).resource
            for c in self.obj.correspondents_having_roles
        ]

    def get_roles_resource_identifiers(self):
        from app.api.correspondent_has_role.facade import CorrespondentHasRoleFacade
        return [] if self.obj.correspondents_having_roles is None else [
            CorrespondentHasRoleFacade.make_resource_identifier(e.id, CorrespondentHasRoleFacade.TYPE)
            for e in self.obj.correspondents_having_roles]

    def get_roles_resources(self):
        from app.api.correspondent_has_role.facade import CorrespondentHasRoleFacade
        return [] if self.obj.correspondents_having_roles is None else [CorrespondentHasRoleFacade(self.url_prefix, e,
                                                                                                   self.with_relationships_links,
                                                                                                   self.with_relationships_data).resource
                                                                        for e in self.obj.correspondents_having_roles]

    @property
    def resource(self):
        resource = {
            **self.resource_identifier,
            "attributes": {
                "firstname": self.obj.firstname,
                "lastname": self.obj.lastname,
                "key": self.obj.key,
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
        super(CorrespondentFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is a correspondent
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

            "firstname": _res["attributes"]["firstname"],
            "lastname": _res["attributes"]["lastname"],
            "ref": _res["attributes"]["ref"],
            "key": _res["attributes"]["key"],
        }
        correspondent_data = [{"id": _res["id"], "index": self.get_index_name(), "payload": payload}]
        if not propagate:
            return correspondent_data
        else:
            return correspondent_data + self.get_relationship_data_to_index(rel_name="documents")

    def remove_from_index(self, propagate):
        from app.search import SearchIndexManager
        SearchIndexManager.remove_from_index(index=self.get_index_name(), id=self.id)

        if propagate:
            # reindex the docs without the resource
            for data in self.get_data_to_index_when_added():
                if data["payload"]["id"] != self.id and data["payload"]["type"] != self.TYPE:
                    data["payload"]["correspondents"] = [l for l in data["payload"]["correspondents"] if l.get("id") != self.id]
                    SearchIndexManager.add_to_index(index=data["index"], id=data["id"], payload=data["payload"])