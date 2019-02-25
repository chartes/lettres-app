import pprint

from app import db
from app.api.abstract_facade import JSONAPIAbstractChangeloggedFacade
from app.models import Language


class LanguageFacade(JSONAPIAbstractChangeloggedFacade):
    """

    """
    TYPE = "language"
    TYPE_PLURAL = "languages"

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def get_resource_facade(url_prefix, id, **kwargs):
        e = Language.query.filter(Language.id == id).first()
        if e is None:
            kwargs = {"status": 404}
            errors = [{"status": 404, "title": "language %s does not exist" % id}]
        else:
            e = LanguageFacade(url_prefix, e, **kwargs)
            kwargs = {}
            errors = []
        return e, kwargs, errors

    @property
    def resource(self):
        resource = {
            **self.resource_identifier,
            "attributes": {
                "code": self.obj.code,
                "label": self.obj.label
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
        super(LanguageFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is a language
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

            "code": _res["attributes"]["code"],
            "label": _res["attributes"]["label"],
        }
        languages_data = [{"id": _res["id"], "index": self.get_index_name(), "payload": payload}]
        if not propagate:
            return languages_data
        else:
            return languages_data + self.get_relationship_data_to_index(rel_name="documents")

    def remove_from_index(self, propagate):
        from app.search import SearchIndexManager

        SearchIndexManager.remove_from_index(index=self.get_index_name(), id=self.id)

        if propagate:
            # reindex the docs without the resource
            for data in self.get_data_to_index_when_added(propagate):
                if data["payload"]["id"] != self.id and data["payload"]["type"] != self.TYPE:
                    data["payload"]["languages"] = [l for l in data["payload"]["languages"] if l.get("id") != self.id]
                    SearchIndexManager.add_to_index(index=data["index"], id=data["id"], payload=data["payload"])