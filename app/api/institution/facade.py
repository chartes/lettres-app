from app.api.abstract_facade import JSONAPIAbstractFacade
from app.models import Institution


class InstitutionFacade(JSONAPIAbstractFacade):
    """

    """
    TYPE = "institution"
    TYPE_PLURAL = "institutions"

    MODEL = Institution

    @property
    def id(self):
        return self.obj.id

    #@staticmethod
    #def get_resource_facade(url_prefix, id, **kwargs):
    #    e = Institution.query.filter(Institution.id == id).first()
    #    if e is None:
    #        kwargs = {"status": 404}
    #        errors = [{"status": 404, "title": "institution %s does not exist" % id}]
    #    else:
    #        e = InstitutionFacade(url_prefix, e, **kwargs)
    #        kwargs = {}
    #        errors = []
    #    return e, kwargs, errors

    @property
    def resource(self):
        resource = {
            **self.resource_identifier,
            "attributes": {
                "name": self.obj.name,
                "ref": self.obj.ref
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
        super(InstitutionFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is an institution
        """

        from app.api.witness.facade import WitnessFacade

        self.relationships = {
            "witnesses": {
                "links": self._get_links(rel_name="witnesses"),
                "resource_identifier_getter":  self.get_related_resource_identifiers(WitnessFacade, "witnesses", to_many=True),
                "resource_getter":  self.get_related_resources(WitnessFacade, "witnesses", to_many=True),
            }
        }

    def get_data_to_index_when_added(self, propagate):
        _res = self.resource
        payload = {
            "id": _res["id"],
            "type": _res["type"],

            "name": _res["attributes"]["name"],
            "ref": _res["attributes"]["ref"],
        }
        institution_data = [{"id": _res["id"], "index": self.get_index_name(), "payload": payload}]
        return institution_data

    def remove_from_index(self, propagate):
        from app.api.search import SearchIndexManager
        SearchIndexManager.remove_from_index(index=self.get_index_name(), id=self.id)
