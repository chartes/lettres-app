from app.api.abstract_facade import JSONAPIAbstractChangeloggedFacade
from app.api.user.facade import UserFacade
from app.models import Collection


class CollectionFacade(JSONAPIAbstractChangeloggedFacade):
    """

    """
    TYPE = "collection"
    TYPE_PLURAL = "collections"

    MODEL = Collection

    @property
    def id(self):
        return self.obj.id

    #@staticmethod
    #def get_resource_facade(url_prefix, id, **kwargs):
    #    e = Collection.query.filter(Collection.id == id).first()
    #    if e is None:
    #        kwargs = {"status": 404}
    #        errors = [{"status": 404, "title": "Collection %s does not exist" % id}]
    #    else:
    #        e = CollectionFacade(url_prefix, e, **kwargs)
    #        kwargs = {}
    #        errors = []
    #    return e, kwargs, errors

    def get_parents_resource_identifiers(self, rel_facade=None):
        parents = self.obj.parents
        rel_facade = CollectionFacade if not rel_facade else rel_facade

        return [] if parents is None else [
            rel_facade.make_resource_identifier(parent.id, rel_facade.TYPE)
            for parent in parents
        ]

    def get_children_resource_identifiers(self, rel_facade=None):
        children = self.obj.children
        rel_facade = CollectionFacade if not rel_facade else rel_facade

        return [] if children is None else [
            rel_facade.make_resource_identifier(child.id, rel_facade.TYPE)
            for child in children
        ]

    def get_parents_resources(self, rel_facade=None):
        parents = self.obj.parents
        rel_facade = CollectionFacade if not rel_facade else rel_facade

        return [] if parents is None else [
            rel_facade(self.url_prefix, parent, self.with_relationships_links,
                       self.with_relationships_data).resource
            for parent in parents
        ]

    def get_children_resources(self, rel_facade=None):
        children = self.obj.children
        rel_facade = CollectionFacade if not rel_facade else rel_facade

        return [] if children is None else [
            rel_facade(self.url_prefix, child, self.with_relationships_links,
                       self.with_relationships_data).resource
            for child in children
        ]

    @property
    def resource(self):

        resource = {
            **self.resource_identifier,
            "attributes": {
                "title": self.obj.title,
                "description": self.obj.description,
                "nb_docs": len(self.obj.documents_including_children),
                "date_min": min([doc.creation for doc in self.obj.documents_including_children]),
                "date_max": max([doc.creation for doc in self.obj.documents_including_children])
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
        super(CollectionFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is a Collection
        """

        from app.api.document.facade import DocumentFacade

        self.relationships.update({
            "documents": {
                "links": self._get_links(rel_name="documents"),
                "resource_identifier_getter": self.get_related_resource_identifiers(DocumentFacade, "documents", to_many=True),
                "resource_getter": self.get_related_resources(DocumentFacade, "documents", to_many=True),
            },
            "documents-including-children": {
                "links": self._get_links(rel_name="documents-including-children"),
                "resource_identifier_getter": self.get_related_resource_identifiers(DocumentFacade, "documents_including_children",
                                                                                    to_many=True),
                "resource_getter": self.get_related_resources(DocumentFacade, "documents_including_children", to_many=True),
            },
            "admin": {
                "links": self._get_links(rel_name="admin"),
                "resource_identifier_getter": self.get_related_resource_identifiers(UserFacade, "admin", to_many=False),
                "resource_getter": self.get_related_resources(UserFacade, "admin", to_many=False),
            },
            "parents": {
                "links": self._get_links(rel_name="parents"),
                "resource_identifier_getter": self.get_parents_resource_identifiers,
                "resource_getter": self.get_parents_resources,
            },
            "children": {
                "links": self._get_links(rel_name="children"),
                "resource_identifier_getter": self.get_children_resource_identifiers,
                "resource_getter": self.get_children_resources,
            }
        })

    def get_data_to_index_when_added(self, propagate):
        _res = self.resource
        payload = {
            "id": _res["id"],
            "type": _res["type"],

            "title": _res["attributes"]["title"],
            "description": _res["attributes"]["description"],
        }
        collection_data = [{"id": _res["id"], "index": self.get_index_name(), "payload": payload}]
        if not propagate:
            return collection_data
        else:
            return collection_data + self.get_relationship_data_to_index(rel_name="documents")

    def remove_from_index(self, propagate):
        from app.api.search import SearchIndexManager
        SearchIndexManager.remove_from_index(index=self.get_index_name(), id=self.id)

        if propagate:
            # reindex the docs without the resource
            for data in self.get_data_to_index_when_added(propagate):
                if data["payload"]["id"] != self.id and data["payload"]["type"] != self.TYPE:
                    data["payload"]["collections"] = [l for l in data["payload"]["collections"] if l.get("id") != self.id]
                    SearchIndexManager.add_to_index(index=data["index"], id=data["id"], payload=data["payload"])
