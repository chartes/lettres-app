from app import db
from app.api.abstract_facade import JSONAPIAbstractFacade
from app.models import Correspondent, CorrespondentRole


class CorrespondentRoleFacade(JSONAPIAbstractFacade):
    """

    """
    TYPE = "correspondent-role"
    TYPE_PLURAL = "correspondent-roles"

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def get_resource_facade(url_prefix, id, **kwargs):
        e = CorrespondentRole.query.filter(CorrespondentRole.id == id).first()
        if e is None:
            kwargs = {"status": 404}
            errors = [{"status": 404, "title": "correspondent role %s does not exist" % id}]
        else:
            e = CorrespondentRoleFacade(url_prefix, e, **kwargs)
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
            co = Correspondent(
                id=id,
                label=_g("label"),
                description=_g("description"),
            )
            db.session.add(co)
            db.session.commit()
            resource = co
        except Exception as e:
            print(e)
            errors = [{"status": 403, "title": "Error creating resource 'CorrespondentRole' with data: %s" % (str([id, attributes, related_resources]))}]
            db.session.rollback()
        return resource, errors


    def __init__(self, *args, **kwargs):
        super(CorrespondentRoleFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is a correspondent role

        A document is made of:
        attributes:
            id:
            label:
            description:
        relationships:
            roles
        Returns
        -------
            A dict describing the corresponding JSONAPI resource object
        """

        self.relationships = {

        }
        self.resource = {
            **self.resource_identifier,
            "attributes": {
                "id": self.obj.id,
                "label": self.obj.label,
                "description": self.obj.description
            },
            "meta": self.meta,
            "links": {
                "self": self.self_link
            }
        }

        if self.with_relationships_links:
            self.resource["relationships"] = self.get_exposed_relationships()
