from app import db
from app.api.abstract_facade import JSONAPIAbstractChangeloggedFacade
from app.models import Collection


class CollectionFacade(JSONAPIAbstractChangeloggedFacade):
    """

    """
    TYPE = "collection"
    TYPE_PLURAL = "collections"

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def get_resource_facade(url_prefix, id, **kwargs):
        e = Collection.query.filter(Collection.id == id).first()
        if e is None:
            kwargs = {"status": 404}
            errors = [{"status": 404, "title": "Collection %s does not exist" % id}]
        else:
            e = CollectionFacade(url_prefix, e, **kwargs)
            kwargs = {}
            errors = []
        return e, kwargs, errors

    @property
    def resource(self):
        resource = {
            **self.resource_identifier,
            "attributes": {
                "title": self.obj.title,
                "description": self.obj.description
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
        from app.search import SearchIndexManager
        SearchIndexManager.remove_from_index(index=self.get_index_name(), id=self.id)

        if propagate:
            # reindex the docs without the resource
            for data in self.get_data_to_index_when_added():
                if data["payload"]["id"] != self.id and data["payload"]["type"] != self.TYPE:
                    data["payload"]["collections"] = [l for l in data["payload"]["collections"] if l.get("id") != self.id]
                    SearchIndexManager.add_to_index(index=data["index"], id=data["id"], payload=data["payload"])