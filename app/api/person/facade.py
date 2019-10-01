
from app.api.abstract_facade import JSONAPIAbstractChangeloggedFacade, JSONAPIAbstractFacade
from app.models import Person


class PersonFacade(JSONAPIAbstractChangeloggedFacade):
    """

    """
    TYPE = "person"
    TYPE_PLURAL = "persons"

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def get_resource_facade(url_prefix, id, **kwargs):
        e = Person.query.filter(Person.id == id).first()
        if e is None:
            kwargs = {"status": 404}
            errors = [{"status": 404, "title": "person %s does not exist" % id}]
        else:
            e = PersonFacade(url_prefix, e, **kwargs)
            kwargs = {}
            errors = []
        return e, kwargs, errors

    @staticmethod
    def update_resource(obj, obj_type, attributes, related_resources, append=False):
        # rename the relationship
        if "roles-within-documents" in related_resources:
            related_resources["persons_having_roles"] = related_resources.pop("roles-within-documents")
        return JSONAPIAbstractFacade.update_resource(obj, obj_type, attributes, related_resources, append)

    def get_document_resource_identifiers(self):
        from app.api.document.facade import DocumentFacade
        return [] if self.obj.persons_having_roles is None else [
            DocumentFacade.make_resource_identifier(c_h_r.document.id, DocumentFacade.TYPE)
            for c_h_r in self.obj.persons_having_roles
        ]

    def get_document_resources(self):
        from app.api.document.facade import DocumentFacade
        return [] if self.obj.persons_having_roles is None else [
            DocumentFacade(self.url_prefix, c.document, self.with_relationships_links,
                           self.with_relationships_data).resource
            for c in self.obj.persons_having_roles
        ]

    def get_roles_resource_identifiers(self):
        from app.api.person_has_role.facade import PersonHasRoleFacade
        return [] if self.obj.persons_having_roles is None else [
            PersonHasRoleFacade.make_resource_identifier(e.id, PersonHasRoleFacade.TYPE)
            for e in self.obj.persons_having_roles]

    def get_roles_resources(self):
        from app.api.person_has_role.facade import PersonHasRoleFacade
        return [] if self.obj.persons_having_roles is None else [PersonHasRoleFacade(self.url_prefix, e,
                                                                                            self.with_relationships_links,
                                                                                            self.with_relationships_data).resource
                                                                        for e in self.obj.persons_having_roles]

    @property
    def resource(self):
        resource = {
            **self.resource_identifier,
            "attributes": {
                "label": self.obj.label,
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
        super(PersonFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is a person
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
            "label": _res["attributes"]["label"],
        }
        person_data = [{"id": _res["id"], "index": self.get_index_name(), "payload": payload}]
        if not propagate:
            return person_data
        else:
            return person_data + self.get_relationship_data_to_index(rel_name="documents") + self.get_relationship_data_to_index(
                rel_name="roles-within-documents")

    def remove_from_index(self, propagate):
        from app.search import SearchIndexManager
        SearchIndexManager.remove_from_index(index=self.get_index_name(), id=self.id)

        if propagate:
            # reindex the docs without the resource
            for data in self.get_data_to_index_when_added(propagate):
                if data["payload"]["id"] != self.id and data["payload"]["type"] != self.TYPE:
                    data["payload"]["persons"] = [l for l in data["payload"]["persons"] if l.get("id") != self.id]
                    SearchIndexManager.add_to_index(index=data["index"], id=data["id"], payload=data["payload"])
