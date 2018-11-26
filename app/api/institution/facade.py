from app import db
from app.api.abstract_facade import JSONAPIAbstractFacade
from app.models import Institution


class InstitutionFacade(JSONAPIAbstractFacade):
    """

    """
    TYPE = "institution"
    TYPE_PLURAL = "institutions"

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def get_resource_facade(url_prefix, id, **kwargs):
        e = Institution.query.filter(Institution.id == id).first()
        if e is None:
            kwargs = {"status": 404}
            errors = [{"status": 404, "title": "institution %s does not exist" % id}]
        else:
            e = InstitutionFacade(url_prefix, e, **kwargs)
            kwargs = {}
            errors = []
        return e, kwargs, errors

    # noinspection PyArgumentList
    @staticmethod
    def create_resource(id, attributes, related_resources):
        resource = None
        errors = None
        try:
            _g = attributes.get
            co = Institution(
                id=id,
                name=_g("name"),
                ref=_g("ref"),
            )
            db.session.add(co)
            db.session.commit()
            resource = co
        except Exception as e:
            print(e)
            errors = [{"status": 403, "title": "Error creating resource 'Institution' with data: %s" % (
                str([id, attributes, related_resources]))}]
            db.session.rollback()
        return resource, errors

    def __init__(self, *args, **kwargs):
        super(InstitutionFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is an institution
        """

        self.relationships = {

        }
        self.resource = {
            **self.resource_identifier,
            "attributes": {
                "id": self.obj.id,
                "name": self.obj.name,
                "ref": self.obj.ref
            },
            "meta": self.meta,
            "links": {
                "self": self.self_link
            }
        }

        if self.with_relationships_links:
            self.resource["relationships"] = self.get_exposed_relationships()
