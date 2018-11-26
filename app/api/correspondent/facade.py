from app import db
from app.api.abstract_facade import JSONAPIAbstractFacade
from app.models import Correspondent


class CorrespondentFacade(JSONAPIAbstractFacade):
    """

    """
    TYPE = "correspondent"
    TYPE_PLURAL = "correspondents"

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def get_resource_facade(url_prefix, id, **kwargs):
        e = Correspondent.query.filter(Correspondent.id == id).first()
        if e is None:
            kwargs = {"status": 404}
            errors = [{"status": 404, "title": "correspondent %s does not exist" % id}]
        else:
            e = CorrespondentFacade(url_prefix, e, **kwargs)
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
                firstname=_g("title"),
                lastname=_g("subtitle"),
                key=_g("key"),
                ref=_g("ref")
            )
            co.roles = related_resources.get("roles")
            co.document = related_resources.get("documents")
            db.session.add(co)
            db.session.commit()
            resource = co
        except Exception as e:
            print(e)
            errors = [{"status": 403, "title": "Error creating resource 'Correspondent' with data: %s" % (str([id, attributes, related_resources]))}]
            db.session.rollback()
        return resource, errors

    def get_roles_resource_identifiers(self):
        from app.api.correspondent_has_role.facade import CorrespondentHasRoleFacade
        return [] if self.obj.correspondents_have_roles is None else [CorrespondentHasRoleFacade.make_resource_identifier(e.id, CorrespondentHasRoleFacade.TYPE)
                                                    for e in self.obj.correspondents_have_roles]

    def get_roles_resources(self):
        from app.api.correspondent_has_role.facade import CorrespondentHasRoleFacade
        return [] if self.obj.correspondents_have_roles is None else [CorrespondentHasRoleFacade(self.url_prefix, e,
                                                                 self.with_relationships_links,
                                                                 self.with_relationships_data).resource
                                                    for e in self.obj.correspondents_have_roles]

    def __init__(self, *args, **kwargs):
        super(CorrespondentFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is a correspondent

        A document is made of:
        attributes:
            id:
            name:
        relationships:
            roles
        Returns
        -------
            A dict describing the corresponding JSONAPI resource object
        """

        self.relationships = {
            "roles-within-document": {
                "links": self._get_links(rel_name="roles-within-document"),
                "resource_identifier_getter": self.get_roles_resource_identifiers,
                "resource_getter": self.get_roles_resources
            },
        }
        self.resource = {
            **self.resource_identifier,
            "attributes": {
                "id": self.obj.id,
                "firstname": self.obj.firstname,
                "lastname": self.obj.lastname,
                "key": self.obj.key,
                "ref": self.obj.ref,
            },
            "meta": self.meta,
            "links": {
                "self": self.self_link
            }
        }

        if self.with_relationships_links:
            self.resource["relationships"] = self.get_exposed_relationships()
