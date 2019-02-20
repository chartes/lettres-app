
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

    @property
    def resource(self):
        resource = {
            **self.resource_identifier,
            "attributes": {
                "label": self.obj.label,
                "description": self.obj.description,
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
        })

    def get_data_to_index_when_added(self, propagate):
        _res = self.resource
        payload = {
            "id": _res["id"],
            "type": _res["type"],

            "label": _res["attributes"]["label"],
            "description": _res["attributes"]["description"],
            "ref": _res["attributes"]["ref"],
        }
        placename_data = [{"id": _res["id"], "index": self.get_index_name(), "payload": payload}]
        if not propagate:
            return placename_data
        else:
            return placename_data + self.get_relationship_data_to_index(rel_name="documents")

    def remove_from_index(self, propagate):
        from app.search import SearchIndexManager
        SearchIndexManager.remove_from_index(index=self.get_index_name(), id=self.id)

        if propagate:
            # reindex the docs without the resource
            for data in self.get_data_to_index_when_added():
                if data["payload"]["id"] != self.id and data["payload"]["type"] != self.TYPE:
                    data["payload"]["placenames"] = [l for l in data["payload"]["placenames"] if l.get("id") != self.id]
                    SearchIndexManager.add_to_index(index=data["index"], id=data["id"], payload=data["payload"])