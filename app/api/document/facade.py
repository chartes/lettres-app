import requests
import re
from flask import current_app, request

from app.api.abstract_facade import JSONAPIAbstractChangeloggedFacade
from app.api.witness.facade import WitnessFacade
from app.models import Document, WITNESS_STATUS_VALUES

clean_tags = re.compile('<.*?>')
clean_notes = re.compile('\[\d+\]')
clean_page_breaks = re.compile('\[p\.?\s?\d+\]')

def remove_html_tags(text):
    without_unbreakable_space = text.replace('\ufeff','') if text else None
    without_html_content = re.sub(clean_tags,'', without_unbreakable_space) if text else None
    without_without_notes = without_html_content.replace("[note]","").strip() if without_html_content else None
    without_numbered_notes = re.sub(clean_notes,' ', without_without_notes) if without_without_notes else None
    without_page_breaks = re.sub(clean_page_breaks,' ', without_numbered_notes) if without_numbered_notes else None
    cleaned = re.sub(' +', ' ', without_page_breaks) if without_page_breaks else None
    return cleaned

class DocumentFacade(JSONAPIAbstractChangeloggedFacade):
    """

    """
    TYPE = "document"
    TYPE_PLURAL = "documents"

    MODEL = Document

    @property
    def id(self):
        return self.obj.id

    def get_persons_having_roles_resource_identifiers(self, rel_facade=None):
        from app.api.person_has_role.facade import PersonHasRoleFacade
        rel_facade = PersonHasRoleFacade if not rel_facade else rel_facade

        return [] if self.obj.persons_having_roles is None else [
            rel_facade.make_resource_identifier(c.id, rel_facade.TYPE)
            for c in self.obj.persons_having_roles
        ]

    def get_persons_having_roles_resources(self, rel_facade=None):
        from app.api.person_has_role.facade import PersonHasRoleFacade
        rel_facade = PersonHasRoleFacade if not rel_facade else rel_facade

        return [] if self.obj.persons_having_roles is None else [
            rel_facade(self.url_prefix, c, True, True).resource
            for c in self.obj.persons_having_roles
        ]

    def get_person_role_resource_identifiers(self, rel_facade=None):
        from app.api.person_role.facade import PersonRoleFacade
        rel_facade = PersonRoleFacade if not rel_facade else rel_facade

        return [] if self.obj.persons_having_roles is None else [
            rel_facade.make_resource_identifier(c_h_r.person_role.id, rel_facade.TYPE)
            for c_h_r in self.obj.persons_having_roles
        ]

    def get_person_role_resources(self, rel_facade=None):
        from app.api.person_role.facade import PersonRoleFacade
        rel_facade = PersonRoleFacade if not rel_facade else rel_facade

        return [] if self.obj.persons_having_roles is None else [
            rel_facade(self.url_prefix, c.person_role, self.with_relationships_links,
                             self.with_relationships_data).resource
            for c in self.obj.persons_having_roles
        ]

    def get_placename_role_resource_identifiers(self, rel_facade=None):
        from app.api.placename_role.facade import PlacenameRoleFacade
        rel_facade = PlacenameRoleFacade if not rel_facade else rel_facade

        return [] if self.obj.placenames_having_roles is None else [
            rel_facade.make_resource_identifier(c_h_r.placename_role.id, rel_facade.TYPE)
            for c_h_r in self.obj.placenames_having_roles
        ]

    def get_placename_role_resources(self, rel_facade=None):
        from app.api.placename_role.facade import PlacenameRoleFacade
        rel_facade = PlacenameRoleFacade if not rel_facade else rel_facade

        return [] if self.obj.placenames_having_roles is None else [
            rel_facade(self.url_prefix, c.placename_role, self.with_relationships_links,
                             self.with_relationships_data).resource
            for c in self.obj.placenames_having_roles
        ]

    def get_person_resource_identifiers(self, rel_facade=None):
        from app.api.person.facade import PersonFacade
        rel_facade = PersonFacade if not rel_facade else rel_facade

        return [] if self.obj.persons_having_roles is None else [
            rel_facade.make_resource_identifier(c_h_r.person.id, rel_facade.TYPE)
            for c_h_r in self.obj.persons_having_roles
        ]

    def get_person_resources(self, rel_facade=None):
        from app.api.person.facade import PersonFacade
        rel_facade = PersonFacade if not rel_facade else rel_facade

        return [] if self.obj.persons_having_roles is None else [
            rel_facade(self.url_prefix, c.person, self.with_relationships_links,
                         self.with_relationships_data).resource
            for c in self.obj.persons_having_roles
        ]

    def get_placename_resource_identifiers(self, rel_facade=None):
        from app.api.placename.facade import PlacenameFacade
        rel_facade = PlacenameFacade if not rel_facade else rel_facade

        return [] if self.obj.placenames_having_roles is None else [
            rel_facade.make_resource_identifier(c_h_r.placename.id, rel_facade.TYPE)
            for c_h_r in self.obj.placenames_having_roles
        ]

    def get_placename_resources(self, rel_facade=None):
        from app.api.placename.facade import PlacenameFacade
        rel_facade = PlacenameFacade if not rel_facade else rel_facade

        return [] if self.obj.placenames_having_roles is None else [
            rel_facade(self.url_prefix, c.placename, self.with_relationships_links,
                         self.with_relationships_data).resource
            for c in self.obj.placenames_having_roles
        ]

    def get_placenames_having_roles_resource_identifiers(self, rel_facade=None):
        from app.api.placename_has_role.facade import PlacenameHasRoleFacade
        rel_facade = PlacenameHasRoleFacade if not rel_facade else rel_facade

        return [] if self.obj.placenames_having_roles is None else [
            rel_facade.make_resource_identifier(c.id, rel_facade.TYPE)
            for c in self.obj.placenames_having_roles
        ]

    def get_placenames_having_roles_resources(self, rel_facade=None):
        from app.api.placename_has_role.facade import PlacenameHasRoleFacade
        rel_facade = PlacenameHasRoleFacade if not rel_facade else rel_facade

        return [] if self.obj.placenames_having_roles is None else [
            rel_facade(self.url_prefix, c, True, True).resource
            for c in self.obj.placenames_having_roles
        ]

    def get_first_witness_manifest_url(self):
        w = sorted(self.obj.witnesses, key=lambda k: k.num)
        if len(w) == 0:
            return None
        f_obj, errors, kwargs = WitnessFacade.get_facade('', w[0])
        return f_obj.get_iiif_manifest_url()

    def get_iiif_collection_url(self):
        #return "https://iiif.chartes.psl.eu/collections/encpos/encpos_1892.json"
        host = request.host_url[:-1]
        prefix = current_app.config['IIIF_URL_PREFIX']
        return f"{host}{prefix}/documents/{self.obj.id}/collection"

    def get_iiif_thumbnail(self):
        for w in self.obj.witnesses:
            canvas_ids = [img.canvas_id for img in w.images]
            if canvas_ids:
                from app.api.witness.facade import WitnessFacade
                f_obj, errors, kwargs = WitnessFacade.get_facade('', w)
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
                "transcription": self.obj.transcription,
                "address": self.obj.address,

                "is-published": False if self.obj.is_published is None else self.obj.is_published,

                "iiif-base-witness-manifest-url": self.get_first_witness_manifest_url(),
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
            "persons-having-roles": {
                "links": self._get_links(rel_name="persons-having-roles"),
                "resource_identifier_getter": self.get_persons_having_roles_resource_identifiers,
                "resource_getter": self.get_persons_having_roles_resources
            },
            "person-roles": {
                "links": self._get_links(rel_name="roles"),
                "resource_identifier_getter": self.get_person_role_resource_identifiers,
                "resource_getter": self.get_person_role_resources
            },
            "persons": {
                "links": self._get_links(rel_name="persons"),
                "resource_identifier_getter": self.get_person_resource_identifiers,
                "resource_getter": self.get_person_resources
            },

            "placenames-having-roles": {
                "links": self._get_links(rel_name="placenames-having-roles"),
                "resource_identifier_getter": self.get_placenames_having_roles_resource_identifiers,
                "resource_getter": self.get_placenames_having_roles_resources
            },
            "placename-roles": {
                "links": self._get_links(rel_name="roles"),
                "resource_identifier_getter": self.get_placename_role_resource_identifiers,
                "resource_getter": self.get_placename_role_resources
            },
            "placenames": {
                "links": self._get_links(rel_name="placenames"),
                "resource_identifier_getter": self.get_placename_resource_identifiers,
                "resource_getter": self.get_placename_resources
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
            "current-lock": (LockFacade, False)
        }.items():
            u_rel_name = rel_name.replace("-", "_")

            self.relationships[rel_name] = {
                "links": self._get_links(rel_name=rel_name),
                "resource_identifier_getter": self.get_related_resource_identifiers(rel_facade, u_rel_name, to_many),
                "resource_getter": self.get_related_resources(rel_facade, u_rel_name, to_many),
            }

    def get_data_to_index_when_added(self, propagate):
        #_res = self.resource
        payload = {
            "id": self.id,
            "type": self.TYPE,

            "is-published": False if self.obj.is_published is None else self.obj.is_published,

            "creation": self.obj.creation,
            "creation-not-after": self.obj.creation_not_after,

            "title": remove_html_tags(self.obj.title),
            "argument": remove_html_tags(self.obj.argument),
            "transcription": remove_html_tags(self.obj.transcription),
            "address": remove_html_tags(self.obj.address),

            "witnesses": [{"id": w.id, "content": w.content, "classification-mark": w.classification_mark} for w in self.obj.witnesses],
            "languages": [{"id": l.id, "code": l.code} for l in self.obj.languages],
            "collections": [{"id": c.id, "title": c.title} for c in self.obj.collections],
            "persons": [
                {
                    "id": c_h_r.person.id,
                    "label": c_h_r.person.label,
                    "ref": c_h_r.person.ref
                }
                for c_h_r in self.obj.persons_having_roles
            ],
            "recipients": [
                {
                    "id": c_h_r.person.id,
                    "label": c_h_r.person.label,
                    "ref": c_h_r.person.ref
                }
                for c_h_r in self.obj.persons_having_roles if c_h_r.person_role.label == 'recipient'
            ],
            "senders": [
                {
                    "id": c_h_r.person.id,
                    "label": c_h_r.person.label,
                    "ref": c_h_r.person.ref
                }
                for c_h_r in self.obj.persons_having_roles if c_h_r.person_role.label == 'sender'
            ],
            "person-inlined": [
                {
                    "id": c_h_r.person.id,
                    "label": c_h_r.person.label,
                    "ref": c_h_r.person.ref
                }
                for c_h_r in self.obj.persons_having_roles if c_h_r.person_role.label == 'inlined'
            ],
            "placenames": [
                {
                    "id": c_h_r.placename.id,
                    "label": c_h_r.placename.label,
                    "ref": c_h_r.placename.ref
                }
                for c_h_r in self.obj.placenames_having_roles
            ],
            "location-date-from": [
                {
                    "id": c_h_r.placename.id,
                    "label": c_h_r.placename.label,
                    "ref": c_h_r.placename.ref
                }
                for c_h_r in self.obj.placenames_having_roles if c_h_r.placename_role.label == 'location-date-from'
            ],
            "location-date-to": [
                {
                    "id": c_h_r.placename.id,
                    "label": c_h_r.placename.label,
                    "ref": c_h_r.placename.ref
                }
                for c_h_r in self.obj.placenames_having_roles if c_h_r.placename_role.label == 'location-date-to'
            ],
            "location-inlined": [
                {
                    "id": c_h_r.placename.id,
                    "label": c_h_r.placename.label,
                    "ref": c_h_r.placename.ref
                }
                for c_h_r in self.obj.placenames_having_roles if c_h_r.placename_role.label == 'inlined'
            ]
        }
        return [{"id": self.obj.id, "index": self.get_index_name(), "payload": payload}]

    def get_data_to_index_when_removed(self, propagate):
        #print("GOING TO BE REMOVED FROM INDEX:", [{"id": self.obj.id, "index": self.get_index_name()}])
        return [{"id": self.obj.id, "index": self.get_index_name()}]


class DocumentSearchFacade(DocumentFacade):
    def __init__(self, *args, **kwargs):
        super(DocumentSearchFacade, self).__init__(*args, **kwargs)
        self.relationships.pop("current-lock")
        self.relationships.pop("changes")

    @property
    def resource(self):
        """
        remove the thumbnail generation from the attributes
        :return:
        """
        """TODO: send directly senders etc in response ? "senders": [
                            {
                                "id": c_h_r.person.id,
                                "label": c_h_r.person.label,
                                "ref": c_h_r.person.ref
                            }
                            for c_h_r in self.obj.persons_having_roles if c_h_r.person_role.label == 'sender'
                        ],"""
        resource = {
            **self.resource_identifier,
            "attributes": {
                "title": self.obj.title,
                "argument": self.obj.argument,
                "creation": self.obj.creation,
                "creation-not-after": self.obj.creation_not_after,
                "creation-label": self.obj.creation_label,
                #"transcription": self.obj.transcription,
                #"address": self.obj.address,
                "is-published": False if self.obj.is_published is None else self.obj.is_published,
                #"iiif-thumbnail-url": self.get_iiif_thumbnail()
            },
            "meta": self.meta,
            "links": {
                "self": self.self_link
            }
        }
        if self.with_relationships_links:
            resource["relationships"] = self.get_exposed_relationships()
        return resource


class DocumentStatusFacade(DocumentFacade):
    def __init__(self, *args, **kwargs):
        super(DocumentStatusFacade, self).__init__(*args, **kwargs)
        self.relationships = {
            "current-lock": self.relationships["current-lock"]
        }

    @property
    def resource(self):
        resource = {
            **self.resource_identifier,
            "attributes": {
                "is-published": False if self.obj.is_published is None else self.obj.is_published,
            },
            "meta": self.meta,
            "links": {
                "self": self.self_link
            }
        }
        if self.with_relationships_links:
            resource["relationships"] = self.get_exposed_relationships()
        return resource


class DocumentBookmarkFacade(DocumentFacade):

    def __init__(self, *args, **kwargs):
        super(DocumentFacade, self).__init__(*args, **kwargs)
        self.relationships = {

        }

    #@staticmethod
    #def get_resource_facade(url_prefix, id, **kwargs):
    #    e = Document.query.filter(Document.id == id).first()
    #    if e is None:
    #        kwargs = {"status": 404}
    #        errors = [{"status": 404, "title": "document %s does not exist" % id}]
    #    else:
    #        e = DocumentBookmarkFacade(url_prefix, e, **kwargs)
    #        kwargs = {}
    #        errors = []
    #    return e, kwargs, errors

    @property
    def resource(self):
        """
        rappel :
        adresse = à qui s'adresse la lettre
        argument = analyse
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
                "is-published": False if self.obj.is_published is None else self.obj.is_published,
            },
            "meta": self.meta,
            "links": {
                "self": self.self_link
            }
        }

        if self.with_relationships_links:
            resource["relationships"] = self.get_exposed_relationships()

        return resource
