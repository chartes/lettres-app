from app import db
from app.api.abstract_facade import JSONAPIAbstractFacade
from app.models import Correspondent, CorrespondentHasRole


class CorrespondentHasRoleFacade(JSONAPIAbstractFacade):
    """

    """
    TYPE = "correspondent-has-role"
    TYPE_PLURAL = "correspondents-having-roles"

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def get_resource_facade(url_prefix, id, **kwargs):
        e = CorrespondentHasRole.query.filter(CorrespondentHasRole.id == id).first()
        if e is None:
            kwargs = {"status": 404}
            errors = [{"status": 404, "title": "CorrespondentHasRole %s does not exist" % id}]
        else:
            e = CorrespondentHasRoleFacade(url_prefix, e, **kwargs)
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
            co = CorrespondentHasRole(
                correspondent_id=_g("correspondent-id"),
                document_id=_g("document-id"),
                correspondent_role_id=_g("correspondent-role-id")
            )

            co.correspondent = related_resources.get("correspondent")
            co.document = related_resources.get("document")
            co.document = related_resources.get("role")

            db.session.add(co)
            db.session.commit()
            resource = co
        except Exception as e:
            print(e)
            errors = [{"status": 403, "title": "Error creating resource 'CorrespondentHasRole' with data: %s" % (
                str([id, attributes, related_resources]))}]
            db.session.rollback()
        return resource, errors

    def get_role_resource_identifier(self):
        from app.api.correspondent_role.facade import CorrespondentRoleFacade
        return None if self.obj.correspondent_role is None else CorrespondentRoleFacade.make_resource_identifier(self.obj.correspondent_role.id,
                                                                                                   CorrespondentRoleFacade.TYPE)

    def get_role_resource(self):
        from app.api.correspondent_role.facade import CorrespondentRoleFacade
        return None if self.obj.correspondent_role is None else CorrespondentRoleFacade(self.url_prefix, self.obj.correspondent_role,
                                                                          self.with_relationships_links,
                                                                          self.with_relationships_data).resource

    def get_correspondent_resource_identifier(self):
        from app.api.correspondent.facade import CorrespondentFacade
        return None if self.obj.correspondent is None else CorrespondentFacade.make_resource_identifier(self.obj.correspondent.id,
                                                                                                        CorrespondentFacade.TYPE)

    def get_correspondent_resource(self):
        from app.api.correspondent.facade import CorrespondentFacade
        return None if self.obj.correspondent is None else CorrespondentFacade(self.url_prefix, self.obj.correspondent,
                                                                          self.with_relationships_links,
                                                                          self.with_relationships_data).resource

    def get_document_resource_identifier(self):
        from app.api.document.facade import DocumentFacade
        return None if self.obj.document is None else DocumentFacade.make_resource_identifier(self.obj.document.id,
                                                                                              DocumentFacade.TYPE)

    def get_document_resource(self):
        from app.api.document.facade import DocumentFacade
        return None if self.obj.document is None else DocumentFacade(self.url_prefix, self.obj.document,
                                                                          self.with_relationships_links,
                                                                          self.with_relationships_data).resource

    def __init__(self, *args, **kwargs):
        super(CorrespondentHasRoleFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is the relation between a correspondent and its role within a document
        """

        self.relationships = {
            "role": {
                "links": self._get_links(rel_name="role"),
                "resource_identifier_getter": self.get_role_resource_identifier,
                "resource_getter": self.get_role_resource
            },
            "document": {
                "links": self._get_links(rel_name="role"),
                "resource_identifier_getter": self.get_document_resource_identifier,
                "resource_getter": self.get_document_resource
            },
            "correspondent": {
                "links": self._get_links(rel_name="role"),
                "resource_identifier_getter": self.get_correspondent_resource_identifier,
                "resource_getter": self.get_correspondent_resource
            },
        }
        self.resource = {
            **self.resource_identifier,
            "attributes": {
                "id": self.obj.id
            },
            "meta": self.meta,
            "links": {
                "self": self.self_link
            }
        }

        print(self.with_relationships_data)
        if self.with_relationships_links:
            self.resource["relationships"] = self.get_exposed_relationships()
