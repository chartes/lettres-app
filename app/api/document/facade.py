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
            resource = Document(
                id=id,
                title=_g("title"),
                owner_id=-1
            )
            #images = related_resources.get("images", [])
            #for img in images:
            #    if img.document_id is not None:
            #        raise ValueError("The image '%s' is already linked to document '%s'" % (img.id, img.document_id))
            resource.images = related_resources.get("images", [])
            resource.notes = related_resources.get("notes", [])
            resource.languages = related_resources.get("languages", [])
            resource.institution = related_resources["institution"][0] if related_resources.get("institution") else None
            resource.tradition = related_resources["tradition"][0] if related_resources.get("tradition") else None
            resource.next_document = related_resources["next-document"][0] if related_resources.get("next-document") else None
            resource.owner = related_resources["owner"][0] if related_resources.get("owner") else None
            resource.whitelist = related_resources["whitelist"][0] if related_resources.get("whitelist") else None

            db.session.add(resource)
            db.session.commit()
        except Exception as e:
            print(e)
            errors = {
                "status": 403,
                "title": "Error creating resource 'Document' with data: %s" % str([id, attributes, related_resources]),
                "detail": str(e)
            }
            db.session.rollback()
        return resource, errors

    def get_image_resource_identifiers(self):
        from app.api.image.facade import ImageFacade
        return [] if self.obj.images is None else [
            ImageFacade.make_resource_identifier(c.id, ImageFacade.TYPE)
            for c in self.obj.images
        ]

    def get_image_resources(self):
        from app.api.image.facade import ImageFacade
        return [] if self.obj.images is None else [
            ImageFacade(self.url_prefix, c, self.with_relationships_links, self.with_relationships_data).resource
            for c in self.obj.images
        ]

    def get_note_resource_identifiers(self):
        from app.api.note.facade import NoteFacade
        return [] if self.obj.notes is None else [
            NoteFacade.make_resource_identifier(c.id, NoteFacade.TYPE)
            for c in self.obj.notes
        ]

    def get_note_resources(self):
        from app.api.note.facade import NoteFacade
        return [] if self.obj.notes is None else [
            NoteFacade(self.url_prefix, c, self.with_relationships_links, self.with_relationships_data).resource
            for c in self.obj.notes
        ]

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
                                                                       self.obj.tradition,
                                                                       self.with_relationships_links,
                                                                       self.with_relationships_data).resource

    def get_correspondents_having_roles_resource_identifiers(self):
        from app.api.correspondent_has_role.facade import CorrespondentHasRoleFacade
        return [] if self.obj.correspondents_having_roles is None else [
            CorrespondentHasRoleFacade.make_resource_identifier(c.id, CorrespondentHasRoleFacade.TYPE)
            for c in self.obj.correspondents_having_roles
        ]

    def get_correspondents_having_roles_resources(self):
        from app.api.correspondent_has_role.facade import CorrespondentHasRoleFacade
        return [] if self.obj.correspondents_having_roles is None else [
            CorrespondentHasRoleFacade(self.url_prefix, c, self.with_relationships_links,
                                       self.with_relationships_data).resource
            for c in self.obj.correspondents_having_roles
        ]

    def get_role_resource_identifiers(self):
        from app.api.correspondent_role.facade import CorrespondentRoleFacade
        return [] if self.obj.correspondents_having_roles is None else [
            CorrespondentRoleFacade.make_resource_identifier(c_h_r.correspondent_role.id, CorrespondentRoleFacade.TYPE)
            for c_h_r in self.obj.correspondents_having_roles
        ]

    def get_role_resources(self):
        from app.api.correspondent_role.facade import CorrespondentRoleFacade
        return [] if self.obj.correspondents_having_roles is None else [
            CorrespondentRoleFacade(self.url_prefix, c.correspondent_role, self.with_relationships_links,
                                    self.with_relationships_data).resource
            for c in self.obj.correspondents_having_roles
        ]

    def get_correspondent_resource_identifiers(self):
        from app.api.correspondent.facade import CorrespondentFacade
        return [] if self.obj.correspondents_having_roles is None else [
            CorrespondentFacade.make_resource_identifier(c_h_r.correspondent.id, CorrespondentFacade.TYPE)
            for c_h_r in self.obj.correspondents_having_roles
        ]

    def get_correspondent_resources(self):
        from app.api.correspondent.facade import CorrespondentFacade
        return [] if self.obj.correspondents_having_roles is None else [
            CorrespondentFacade(self.url_prefix, c.correspondent, self.with_relationships_links,
                                self.with_relationships_data).resource
            for c in self.obj.correspondents_having_roles
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

    def get_owner_resource_identifier(self):
        from app.api.user.facade import UserFacade
        return None if self.obj.owner is None else UserFacade.make_resource_identifier(
            self.obj.owner.id, UserFacade.TYPE
        )

    def get_owner_resource(self):
        from app.api.user.facade import UserFacade
        return None if self.obj.owner is None else UserFacade(self.url_prefix,
                                                              self.obj.owner,
                                                              self.with_relationships_links,
                                                              self.with_relationships_data).resource

    def get_whitelist_resource_identifier(self):
        from app.api.whitelist.facade import WhitelistFacade
        return None if self.obj.whitelist is None else WhitelistFacade.make_resource_identifier(
            self.obj.whitelist.id, WhitelistFacade.TYPE
        )

    def get_whitelist_resource(self):
        from app.api.whitelist.facade import WhitelistFacade
        return None if self.obj.whitelist is None else WhitelistFacade(self.url_prefix,
                                                                       self.obj.whitelist,
                                                                       self.with_relationships_links,
                                                                       self.with_relationships_data).resource

    def __init__(self, *args, **kwargs):
        super(DocumentFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is a document
        """

        self.relationships = {
            "images": {
                "links": self._get_links(rel_name="images"),
                "resource_identifier_getter": self.get_image_resource_identifiers,
                "resource_getter": self.get_image_resources,
                "resource_attribute": "images"
            },
            "notes": {
                "links": self._get_links(rel_name="notes"),
                "resource_identifier_getter": self.get_note_resource_identifiers,
                "resource_getter": self.get_note_resources,
                "resource_attribute": "notes"
            },
            "languages": {
                "links": self._get_links(rel_name="languages"),
                "resource_identifier_getter": self.get_language_resource_identifiers,
                "resource_getter": self.get_language_resources,
                "resource_attribute": "languages"
            },
            "institution": {
                "links": self._get_links(rel_name="institution"),
                "resource_identifier_getter": self.get_institution_resource_identifier,
                "resource_getter": self.get_institution_resource,
                "resource_attribute": "institution"
            },
            "tradition": {
                "links": self._get_links(rel_name="tradition"),
                "resource_identifier_getter": self.get_tradition_resource_identifier,
                "resource_getter": self.get_tradition_resource,
                "resource_attribute": "tradition"
            },
            "correspondents-having-roles": {
                "links": self._get_links(rel_name="correspondents-having-roles"),
                "resource_identifier_getter": self.get_correspondents_having_roles_resource_identifiers,
                "resource_getter": self.get_correspondents_having_roles_resources,
                "resource_attribute": "correspondents_having_roles"
            },
            "roles": {
                "links": self._get_links(rel_name="roles"),
                "resource_identifier_getter": self.get_role_resource_identifiers,
                "resource_getter": self.get_role_resources
            },
            "correspondents": {
                "links": self._get_links(rel_name="correspondents"),
                "resource_identifier_getter": self.get_correspondent_resource_identifiers,
                "resource_getter": self.get_correspondent_resources
            },
            "prev-document": {
                "links": self._get_links(rel_name="prev-document"),
                "resource_identifier_getter": self.get_prev_document_resource_identifier,
                "resource_getter": self.get_prev_document_resource
            },
            "next-document": {
                "links": self._get_links(rel_name="next-document"),
                "resource_identifier_getter": self.get_next_document_resource_identifier,
                "resource_getter": self.get_next_document_resource,
                "resource_attribute": "next_document"
            },
            "owner": {
                "links": self._get_links(rel_name="owner"),
                "resource_identifier_getter": self.get_owner_resource_identifier,
                "resource_getter": self.get_owner_resource,
                "resource_attribute": "owner"
            },
            "whitelist": {
                "links": self._get_links(rel_name="whitelist"),
                "resource_identifier_getter": self.get_whitelist_resource_identifier,
                "resource_getter": self.get_whitelist_resource
            },
        }
        self.resource = {
            **self.resource_identifier,
            "attributes": {
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
