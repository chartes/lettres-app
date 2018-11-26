
from app import db
from app.api.abstract_facade import JSONAPIAbstractFacade
from app.models import Document


class DocumentFacade(JSONAPIAbstractFacade):
    """

    """
    TYPE = "document"
    TYPE_PLURAL = "documents"

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def get_resource_facade(url_prefix, id, **kwargs):
        e = Document.query.filter(Document.id == id).first()
        if e is None:
            kwargs = {"status": 404}
            errors = [{"status": 404, "title": "document %s does not exist" % id}]
        else:
            e = DocumentFacade(url_prefix, e, **kwargs)
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
            co = Document(
                id=id,
                title=_g("title")
            )
            db.session.add(co)
            db.session.commit()
            resource = co
        except Exception as e:
            print(e)
            errors = [{"status": 403, "title": "Error creating resource 'Document' with data: %s" % (
                str([id, attributes, related_resources]))}]
            db.session.rollback()
        return resource, errors

    def get_language_resource_identifiers(self):
        from app.api.language.facade import LanguageFacade
        return [] if self.obj.languages is None else [
            LanguageFacade.make_resource_identifier(c.id, LanguageFacade.TYPE)
            for c in self.obj.languages
        ]

    def get_language_resources(self):
        from app.api.language.facade import LanguageFacade
        return [] if self.obj.languages is None else [
            LanguageFacade(self.url_prefix, c, self.with_relationships_links, self.with_relationships_data).resource
            for c in self.obj.languages
        ]

    def get_institution_resource_identifier(self):
        from app.api.institution.facade import InstitutionFacade
        return None if self.obj.institution is None else InstitutionFacade.make_resource_identifier(
            self.obj.institution.id,
            InstitutionFacade.TYPE
        )

    def get_institution_resource(self):
        from app.api.institution.facade import InstitutionFacade
        return None if self.obj.institution is None else InstitutionFacade(self.url_prefix,
                                                                           self.obj.institution,
                                                                           self.with_relationships_links,
                                                                           self.with_relationships_data).resource

    def get_tradition_resource_identifier(self):
        from app.api.tradition.facade import TraditionFacade
        return None if self.obj.tradition is None else TraditionFacade.make_resource_identifier(
            self.obj.institution.id,
            TraditionFacade.TYPE
        )

    def get_tradition_resource(self):
        from app.api.tradition.facade import TraditionFacade
        return None if self.obj.tradition is None else TraditionFacade(self.url_prefix,
                                                                       self.obj.institution,
                                                                       self.with_relationships_links,
                                                                       self.with_relationships_data).resource

    def get_correspondents_have_roles_resource_identifiers(self):
        from app.api.correspondent_has_role.facade import CorrespondentHasRoleFacade
        return [] if self.obj.correspondents_have_roles is None else [
            CorrespondentHasRoleFacade.make_resource_identifier(c.id, CorrespondentHasRoleFacade.TYPE)
            for c in self.obj.correspondents_have_roles
        ]

    def get_correspondents_have_roles_resources(self):
        from app.api.correspondent_has_role.facade import CorrespondentHasRoleFacade
        return [] if self.obj.correspondents_have_roles is None else [
            CorrespondentHasRoleFacade(self.url_prefix, c, self.with_relationships_links, self.with_relationships_data).resource
            for c in self.obj.correspondents_have_roles
        ]

    def get_next_document_resource_identifier(self):
        return None if self.obj.next_document is None else DocumentFacade.make_resource_identifier(
            self.obj.next_document.id, DocumentFacade.TYPE
        )

    def get_next_document_resource(self):
        return None if self.obj.next_document is None else DocumentFacade(self.url_prefix,
                                                                          self.obj.next_document,
                                                                          self.with_relationships_links,
                                                                          self.with_relationships_data).resource

    def get_prev_document_resource_identifier(self):
        return None if self.obj.prev_document is None else DocumentFacade.make_resource_identifier(
            self.obj.prev_document.id, DocumentFacade.TYPE
        )

    def get_prev_document_resource(self):
        return None if self.obj.next_document is None else DocumentFacade(self.url_prefix,
                                                                          self.obj.prev_document,
                                                                          self.with_relationships_links,
                                                                          self.with_relationships_data).resource

    def __init__(self, *args, **kwargs):
        super(DocumentFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is a document
        """

        self.relationships = {
            "languages": {
                "links": self._get_links(rel_name="languages"),
                "resource_identifier_getter": self.get_language_resource_identifiers,
                "resource_getter": self.get_language_resources
            },
            "institution": {
                "links": self._get_links(rel_name="institution"),
                "resource_identifier_getter": self.get_institution_resource_identifier,
                "resource_getter": self.get_institution_resource
            },
            "tradition": {
                "links": self._get_links(rel_name="tradition"),
                "resource_identifier_getter": self.get_tradition_resource_identifier,
                "resource_getter": self.get_tradition_resource
            },
            "correspondents-have-roles": {
                "links": self._get_links(rel_name="correspondents-have-roles"),
                "resource_identifier_getter": self.get_correspondents_have_roles_resource_identifiers,
                "resource_getter": self.get_correspondents_have_roles_resources
            },
            "prev-document": {
                "links": self._get_links(rel_name="prev-document"),
                "resource_identifier_getter": self.get_prev_document_resource_identifier,
                "resource_getter": self.get_prev_document_resource
            },
            "next-document": {
                "links": self._get_links(rel_name="next-document"),
                "resource_identifier_getter": self.get_next_document_resource_identifier,
                "resource_getter": self.get_next_document_resource
            },
            #TO BE DONE
            #"images": {
            #
            #},
            #"notes": {
            #
            #},
            #"whitelist": {
            #
            #},
            #"owner": {
            #
            #}
        }
        self.resource = {
            **self.resource_identifier,
            "attributes": {
                "id": self.obj.id,
                "title": self.obj.title,
                "witness-label": self.obj.witness_label,
                "classification-mark": self.obj.classification_mark,
                "argument": self.obj.argument,
                "creation": self.obj.creation,
                "creation-label": self.obj.creation_label,
                "location-date-label": self.obj.location_date_label,
                "location-date-ref": self.obj.location_date_ref,
                "transcription": self.obj.transcription,
                "last-update": self.obj.date_update,
                "is-published": self.obj.is_published,
            },
            "meta": self.meta,
            "links": {
                "self": self.self_link
            }
        }

        if self.with_relationships_links:
            self.resource["relationships"] = self.get_exposed_relationships()
