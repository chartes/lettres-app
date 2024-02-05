from sqlalchemy import and_
from app.api.abstract_facade import JSONAPIAbstractChangeloggedFacade, JSONAPIAbstractFacade
from app.models import Person


class PersonFacade(JSONAPIAbstractChangeloggedFacade):
    """

    """
    TYPE = "person"
    TYPE_PLURAL = "persons"

    MODEL = Person

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def update_resource(obj, obj_type, attributes, related_resources, append=False):
        # rename the relationship
        if "roles-within-documents" in related_resources:
            related_resources["persons_having_roles"] = related_resources.pop("roles-within-documents")
        return JSONAPIAbstractFacade.update_resource(obj, obj_type, attributes, related_resources, append)

    def get_document_resource_identifiers(self, rel_facade=None):
        from app.api.document.facade import DocumentFacade
        rel_facade = DocumentFacade if not rel_facade else rel_facade

        resIds = [] if self.obj.persons_having_roles is None else [
            rel_facade.make_resource_identifier(c_h_r.document.id, rel_facade.TYPE)
            for c_h_r in self.obj.persons_having_roles
        ]
        return list({object_['id']: object_ for object_ in resIds}.values())

    def get_document_resources(self, rel_facade=None):
        from app.api.document.facade import DocumentFacade
        rel_facade = DocumentFacade if not rel_facade else rel_facade

        resources = [] if self.obj.persons_having_roles is None else [
            rel_facade(self.url_prefix, c.document, self.with_relationships_links,
                       self.with_relationships_data).resource
            for c in self.obj.persons_having_roles
        ]
        return list({object_.id: object_ for object_ in resources}.values())

    def get_roles_resource_identifiers(self, rel_facade=None):
        from app.api.person_has_role.facade import PersonHasRoleFacade
        rel_facade = PersonHasRoleFacade if not rel_facade else rel_facade

        return [] if self.obj.persons_having_roles is None else [
            rel_facade.make_resource_identifier(e.id, rel_facade.TYPE)
            for e in self.obj.persons_having_roles]

    def get_roles_resources(self, rel_facade=None):
        from app.api.person_has_role.facade import PersonHasRoleFacade
        rel_facade = PersonHasRoleFacade if not rel_facade else rel_facade

        return [] if self.obj.persons_having_roles is None else [rel_facade(self.url_prefix, e,
                                                                            self.with_relationships_links,
                                                                            self.with_relationships_data).resource
                                                                 for e in self.obj.persons_having_roles]

    def get_functions_by_personId(self, ids):
        from app.models import PersonHasRole
        phf = (PersonHasRole.query.with_entities(PersonHasRole.function)
               .filter(and_(PersonHasRole.person_id == ids), PersonHasRole.function.isnot(None))
               .distinct()
               .order_by(PersonHasRole.person_id))
        functions = [p[0] for p in phf] if phf else []
        print("\n functions: ", functions)
        return functions

    @property
    def resource(self):
        resource = {
            **self.resource_identifier,
            "attributes": {
                "label": self.obj.label,
                "ref": self.obj.ref,
                "functions": self.get_functions_by_personId(self.obj.id)
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
            "ref": _res["attributes"]["ref"],
        }
        person_data = [{"id": _res["id"], "index": self.get_index_name(), "payload": payload}]
        if not propagate:
            return person_data
        else:
            return person_data + self.get_relationship_data_to_index(
                rel_name="documents") + self.get_relationship_data_to_index(
                rel_name="roles-within-documents")

    def remove_from_index(self, propagate):
        from app.api.search import SearchIndexManager
        SearchIndexManager.remove_from_index(index=self.get_index_name(), id=self.id)

        if propagate:
            # reindex the docs without the resource
            for data in self.get_data_to_index_when_added(propagate):
                if data["payload"]["id"] != self.id and data["payload"]["type"] != self.TYPE:
                    data["payload"]["persons"] = [l for l in data["payload"]["persons"] if l.get("id") != self.id]
                    SearchIndexManager.add_to_index(index=data["index"], id=data["id"], payload=data["payload"])
