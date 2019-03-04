from app.api.abstract_facade import JSONAPIAbstractChangeloggedFacade
from app.models import Witness


class WitnessFacade(JSONAPIAbstractChangeloggedFacade):
    """

    """
    TYPE = "witness"
    TYPE_PLURAL = "witnesses"

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def get_resource_facade(url_prefix, id, **kwargs):
        e = Witness.query.filter(Witness.id == id).first()
        if e is None:
            kwargs = {"status": 404}
            errors = [{"status": 404, "title": "witness %s does not exist" % id}]
        else:
            e = WitnessFacade(url_prefix, e, **kwargs)
            kwargs = {}
            errors = []
        return e, kwargs, errors

    def get_iiif_manifest_url(self):
        if self.obj.images:
            url = "{witness_url}/manifest".format(witness_url=self.self_link)
            _s = url.rindex(self.TYPE)
            return "{0}iiif/{1}".format(url[0:_s], url[_s:])
        else:
            return None

    @property
    def resource(self):
        resource = {
            **self.resource_identifier,
            "attributes": {
                "content": self.obj.content,
                "tradition": self.obj.tradition,
                "classification-mark": self.obj.classification_mark,
                "status": self.obj.status,
                "manifest-url": self.get_iiif_manifest_url(),
                "num": self.obj.num if self.obj.num else 1
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
        super(WitnessFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is a witness
        """

        from app.api.institution.facade import InstitutionFacade
        from app.api.document.facade import DocumentFacade

        self.relationships.update({
            "document": {
                "links": self._get_links(rel_name="document"),
                "resource_identifier_getter": self.get_related_resource_identifiers(DocumentFacade, "document",
                                                                                    to_many=False),
                "resource_getter": self.get_related_resources(DocumentFacade, "document", to_many=False),
            },
            "institution": {
                "links": self._get_links(rel_name="institution"),
                "resource_identifier_getter": self.get_related_resource_identifiers(InstitutionFacade, "institution",
                                                                                    to_many=False),
                "resource_getter": self.get_related_resources(InstitutionFacade, "institution", to_many=False),
            }
        })

    def get_data_to_index_when_added(self, propagate):
        #_res = self.resource
        payload = {
            "id": self.id,
            "type": self.TYPE,

            "tradition": self.obj.tradition,
            "content": self.obj.content,
            "classification_mark": self.obj.classification_mark,
        }
        witnesses_data = [{"id": self.obj.id, "index": self.get_index_name(), "payload": payload}]
        if not propagate:
            return witnesses_data
        else:
            return witnesses_data + self.get_relationship_data_to_index(rel_name="document")

    def remove_from_index(self, propagate):
        from app.search import SearchIndexManager

        SearchIndexManager.remove_from_index(index=self.get_index_name(), id=self.id)

        if propagate:
            # reindex the docs without the resource
            for data in self.get_data_to_index_when_added(propagate):
                if data["payload"]["id"] != self.id and data["payload"]["type"] != self.TYPE:
                    data["payload"]["witnesses"] = [l for l in data["payload"]["witnesses"] if l.get("id") != self.id]
                    SearchIndexManager.add_to_index(index=data["index"], id=data["id"], payload=data["payload"])