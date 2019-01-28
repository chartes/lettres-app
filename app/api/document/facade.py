from flask import current_app

from app import db
from app.api.abstract_facade import JSONAPIAbstractChangeloggedFacade
from app.models import Document


class DocumentFacade(JSONAPIAbstractChangeloggedFacade):
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

    def get_correspondents_having_roles_resource_identifiers(self):
        from app.api.correspondent_has_role.facade import CorrespondentHasRoleFacade
        return [] if self.obj.correspondents_having_roles is None else [
            CorrespondentHasRoleFacade.make_resource_identifier(c.id, CorrespondentHasRoleFacade.TYPE)
            for c in self.obj.correspondents_having_roles
        ]

    def get_correspondents_having_roles_resources(self):
        from app.api.correspondent_has_role.facade import CorrespondentHasRoleFacade
        return [] if self.obj.correspondents_having_roles is None else [
            CorrespondentHasRoleFacade(self.url_prefix, c, True, True).resource
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

    def get_iiif_collection_url(self):
        if self.obj.witnesses:
            url = "{doc_url}/collection/default".format(doc_url=self.self_link)
            _s = url.rindex(self.TYPE)
            return "{0}iiif/{1}".format(url[0:_s], url[_s:])
        else:
            return None

    def get_iiif_thumbnail(self):
        for w in self.obj.witnesses:
            canvas_ids = [img.canvas_id for img in w.images]
            if canvas_ids:
                from app.api.witness.facade import WitnessFacade
                f_obj, errors, kwargs = WitnessFacade.get_facade(self.url_prefix, w)
                manifest_url = f_obj.get_iiif_manifest_url()
                if manifest_url:
                    canvases = current_app.manifest_factory.fetch_canvas(manifest_url, canvas_ids, cache=True)
                    for c in canvases:
                        if "thumbnail" in c:
                            return c["thumbnail"]["@id"]
        return None

    @property
    def resource(self):
        resource = {
            **self.resource_identifier,
            "attributes": {
                "title": self.obj.title,
                "argument": self.obj.argument,
                "creation": self.obj.creation,
                "creation-not-after": self.obj.creation_not_after,
                "creation-label": self.obj.creation_label,
                "location-date-from-ref": self.obj.location_date_from_ref,
                "location-date-to-ref": self.obj.location_date_to_ref,
                "transcription": self.obj.transcription,

                "is-published": self.obj.is_published is not None,

                "iiif-collection-url": self.get_iiif_collection_url(),
                "iiif-thumbnail-url": self.get_iiif_thumbnail()
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
        super(DocumentFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is a document
        """

        self.relationships.update({
            "correspondents-having-roles": {
                "links": self._get_links(rel_name="correspondents-having-roles"),
                "resource_identifier_getter": self.get_correspondents_having_roles_resource_identifiers,
                "resource_getter": self.get_correspondents_having_roles_resources
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
        })

        # ===================================
        # Add simple relationships
        # ===================================
        from app.api.note.facade import NoteFacade
        from app.api.language.facade import LanguageFacade
        from app.api.witness.facade import WitnessFacade
        from app.api.collection.facade import CollectionFacade
        from app.api.lock.facade import LockFacade

        for rel_name, (rel_facade, to_many) in {
            "collections": (CollectionFacade, True),
            "notes": (NoteFacade, True),
            "languages": (LanguageFacade, True),
            "witnesses": (WitnessFacade, True),
            "prev-document": (DocumentFacade, False),
            "next-document": (DocumentFacade, False),
            "locks": (LockFacade, True)
        }.items():
            u_rel_name = rel_name.replace("-", "_")

            self.relationships[rel_name] = {
                "links": self._get_links(rel_name=rel_name),
                "resource_identifier_getter": self.get_related_resource_identifiers(rel_facade, u_rel_name, to_many),
                "resource_getter": self.get_related_resources(rel_facade, u_rel_name, to_many),
            }

    def get_data_to_index_when_added(self, propagate):
        _res = self.resource
        payload = {
            "id": _res["id"],
            "type": _res["type"],

            "creation": _res["attributes"]["creation"],
            "creation-not-after": _res["attributes"]["creation-not-after"],

            "location-date-from-ref": _res["attributes"]["location-date-from-ref"],
            "location-date-to-ref": _res["attributes"]["location-date-to-ref"],
            "title": _res["attributes"]["title"],
            "argument": _res["attributes"]["argument"],
            "transcription": _res["attributes"]["transcription"],

            "witnesses": [{"id": w.id, "content": w.content} for w in self.obj.witnesses],
            "languages": [{"id": l.id, "code": l.code} for l in self.obj.languages],
            "collections": [{"id": c.id, "title": c.title} for c in self.obj.collections],
            "correspondents": [
                {
                    "id": c_h_r.correspondent.id,
                    "key": c_h_r.correspondent.key,
                    "ref": c_h_r.correspondent.ref
                }
                for c_h_r in self.obj.correspondents_having_roles
            ],
        }
        return [{"id": _res["id"], "index": self.get_index_name(), "payload": payload}]

    def get_data_to_index_when_removed(self, propagate):
        print("GOING TO BE REMOVED FROM INDEX:", [{"id": self.obj.id, "index": self.get_index_name()}])
        return [{"id": self.obj.id, "index": self.get_index_name()}]


class DocumentSearchFacade(DocumentFacade):
    def __init__(self, *args, **kwargs):
        super(DocumentSearchFacade, self).__init__(*args, **kwargs)
        self.relationships.pop("locks")
        self.relationships.pop("changes")

    @property
    def resource(self):
        """
        remove the thumbnail generation from the attributes
        :return:
        """
        resource = {
            **self.resource_identifier,
            "attributes": {
                "title": self.obj.title,
                "argument": self.obj.argument,
                "creation": self.obj.creation,
                "creation-not-after": self.obj.creation_not_after,
                "creation-label": self.obj.creation_label,
                "location-date-from-ref": self.obj.location_date_from_ref,
                "location-date-to-ref": self.obj.location_date_to_ref,
                "transcription": self.obj.transcription,

                "is-published": self.obj.is_published is not None,
            },
            "meta": self.meta,
            "links": {
                "self": self.self_link
            }
        }
        if self.with_relationships_links:
            resource["relationships"] = self.get_exposed_relationships()
        return resource
