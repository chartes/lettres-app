import re
from flask import current_app, request

from app.api.abstract_facade import JSONAPIAbstractChangeloggedFacade
from app.api.witness.facade import WitnessFacade
from app.models import Document, WITNESS_STATUS_VALUES, datetime_to_str

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

    def get_witness_manifest_url(self, id):
        w = [x for x in self.obj.witnesses if x.id == id]
        if len(w) == 0:
            return None
        # do not return a manifest if it has no images
        canvas_ids = [img.canvas_id for img in w[0].images]
        if len(canvas_ids) == 0:
            return None
        f_obj, errors, kwargs = WitnessFacade.get_facade('', w[0])
        return f_obj.get_iiif_manifest_url()

    def get_iiif_manifest(self, id):
        w = [x for x in self.obj.witnesses if x.id == id]
        if len(w) == 0:
            return None
        # do not return a manifest if it has no images
        canvas_ids = [img.canvas_id for img in w[0].images]
        if len(canvas_ids) == 0:
            return None
        f_obj, errors, kwargs = WitnessFacade.get_facade('', w[0])
        manifest, canvas_id = WitnessFacade.get_iiif_manifest(f_obj)
        print("\nmanifest, canvas_id : ", manifest, canvas_id)
        return manifest

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
        date_range = {}
        sort_date = None
        if self.obj.creation and not self.obj.creation_not_after:
            date_range["lte"] = self.obj.creation
            date_range["gte"] = self.obj.creation
            sort_date = self.obj.creation
        else:
            if self.obj.creation_not_after:
                date_range["lte"] = self.obj.creation_not_after
                sort_date = self.obj.creation_not_after
            # for now, if creation_not_after is filled, it means that creation
            # is used as a "creation_not_before"
            if self.obj.creation:
                date_range["gte"] = self.obj.creation
                if sort_date is None:
                    sort_date = self.obj.creation
            # after implementation of creation_not_before in model & data
            # if self.obj.creation_not_before:
                # date_range["gte"] = self.obj.creation_not_before
        locks = []
        if len(self.obj.locks) > 0:
            if len(self.obj.locks) == 1:
                locks = [x.to_document_es_part() for x in self.obj.locks]
            else:
                #upon new lock addition on a previously locked (current or not) document,
                #there are 2 locks (prior previous one is removed)
                #only pick the latest
                current_lock = [l for l in sorted(self.obj.locks, key=lambda k: k.expiration_date, reverse=True) if self.obj.locks][0]
                locks.append(current_lock.to_document_es_part())

        payload = {
            "id": self.id,
            "type": self.TYPE,

            "is-published": False if self.obj.is_published is None else self.obj.is_published,

            "creation": sort_date,
            "creation_range": date_range,
            "creation-not-after": self.obj.creation_not_after,

            "title": remove_html_tags(self.obj.title),
            "argument": remove_html_tags(self.obj.argument),
            "transcription": remove_html_tags(self.obj.transcription),
            "address": remove_html_tags(self.obj.address),

            "witnesses": [{"id": w.id, "content": w.content, "classification-mark": w.classification_mark} for w in sorted(self.obj.witnesses, key=lambda k: k.num) if self.obj.witnesses],
            "languages": [{"id": l.id, "code": l.code} for l in self.obj.languages],
            "collections": [
                {
                    "id": c.id,
                    "parents": [parent.id for parent in c.parents] if c.parents else None
                }
                for c in self.obj.collections
            ],
            "persons": [
                {
                    "id": c_h_r.person.id,
                    #"label": c_h_r.person.label,
                    #"ref": c_h_r.person.ref
                }
                for c_h_r in self.obj.persons_having_roles
            ],
            "senders": [
                {
                    "facet_key": f'{c_h_r.person.id}###{c_h_r.person.label}',
                    "id": c_h_r.person.id,
                    "label": c_h_r.person.label,
                    "ref": c_h_r.person.ref
                }
                for c_h_r in self.obj.persons_having_roles if c_h_r.person_role.label == 'sender'
            ],
            "recipients": [
                {
                    "facet_key": f'{c_h_r.person.id}###{c_h_r.person.label}',
                    "id": c_h_r.person.id,
                    "label": c_h_r.person.label,
                    "ref": c_h_r.person.ref
                }
                for c_h_r in self.obj.persons_having_roles if c_h_r.person_role.label == 'recipient'
            ],
            "persons_inlined": [
                {
                    "facet_key": f'{c_h_r.person.id}###{c_h_r.person.label}',
                    "id": c_h_r.person.id,
                    "label": c_h_r.person.label,
                    "ref": c_h_r.person.ref
                }
                for c_h_r in self.obj.persons_having_roles if c_h_r.person_role.label == 'inlined'
            ],
            "placenames": [
                {
                    "id": c_h_r.placename.id,
                    #"label": c_h_r.placename.label,
                    #"ref": c_h_r.placename.ref
                }
                for c_h_r in self.obj.placenames_having_roles
            ],
            "location_dates_from": [
                {
                    "facet_key": f'{c_h_r.placename.id}###{c_h_r.placename.label}',
                    "id": c_h_r.placename.id,
                    "label": c_h_r.placename.label,
                    "ref": c_h_r.placename.ref
                }
                for c_h_r in self.obj.placenames_having_roles if c_h_r.placename_role.label == 'location-date-from'
            ],
            "location_dates_to": [
                {
                    "facet_key": f'{c_h_r.placename.id}###{c_h_r.placename.label}',
                    "id": c_h_r.placename.id,
                    "label": c_h_r.placename.label,
                    "ref": c_h_r.placename.ref
                }
                for c_h_r in self.obj.placenames_having_roles if c_h_r.placename_role.label == 'location-date-to'
            ],
            "locations_inlined": [
                {
                    "facet_key": f'{c_h_r.placename.id}###{c_h_r.placename.label}',
                    "id": c_h_r.placename.id,
                    "label": c_h_r.placename.label,
                    "ref": c_h_r.placename.ref
                }
                for c_h_r in self.obj.placenames_having_roles if c_h_r.placename_role.label == 'inlined'
            ],
            "lock": locks
        }
        return [{"id": self.obj.id, "index": self.get_index_name(), "payload": payload}]

    def get_data_to_index_when_removed(self, propagate):
        #print("GOING TO BE REMOVED FROM INDEX:", [{"id": self.obj.id, "index": self.get_index_name()}])
        return [{"id": self.obj.id, "index": self.get_index_name()}]

class DocumentFrontFacade(DocumentFacade):
    def __init__(self, *args, **kwargs):
        super(DocumentFrontFacade, self).__init__(*args, **kwargs)
        self.relationships.pop("current-lock")
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
                "creation": self.obj.creation,
                "creation-label": self.obj.creation_label,
                "creation-not-after": self.obj.creation_not_after,
                "argument": self.obj.argument,
                "address": self.obj.address,
                "transcription": self.obj.transcription,
                "is-published": False if self.obj.is_published is None else self.obj.is_published,
                "currentLock": {
                    "id": self.obj.current_lock.id,
                    "description": self.obj.current_lock.description,
                    "event-date": datetime_to_str(self.obj.current_lock.event_date),
                    "expiration-date": datetime_to_str(self.obj.current_lock.expiration_date),
                    "object-id": self.obj.current_lock.object_id,
                    "object-type": self.obj.current_lock.object_type,
                    "is-active": self.obj.current_lock.is_active,
                } if self.obj.current_lock else None,
                "witnesses": [{"id": w.id, "content": w.content, "classification-mark": w.classification_mark, "manifest_url": self.get_witness_manifest_url(w.id), "manifest": self.get_iiif_manifest(w.id), "num": w.num, "status": w.status, "tradition": w.tradition} for w in sorted(self.obj.witnesses, key=lambda k: k.num) if self.obj.witnesses],
                "notes": [{"id": n.id, "content": n.content, "occurences": n.occurences} for n in self.obj.notes],
                "languages": [{"id": l.id, "code": l.code, "label": l.label} for l in self.obj.languages],
                "collections": [
                    {
                        "id": c.id,
                        "title": c.title,
                        "description": c.description,
                    }
                    for c in self.obj.collections
                ],
                "persons": [
                    {
                        "person":
                            {
                                "id": c_h_r.person.id,
                                "label": c_h_r.person.label,
                                "ref": c_h_r.person.ref
                            },
                        "relation":
                            {
                                "field": c_h_r.field,
                                "function": c_h_r.function,
                                "id": c_h_r.id
                            },
                        "role":
                            {
                                "description": c_h_r.person_role.description,
                                "id": c_h_r.person_role.id,
                                "label": c_h_r.person_role.label
                            }
                    }
                    for c_h_r in self.obj.persons_having_roles
                ],
                "placenames": [
                    {
                        "placename":
                            {
                                "id": c_h_r.placename.id,
                                "label": c_h_r.placename.label,
                                "lat": c_h_r.placename.lat,
                                "long": c_h_r.placename.long,
                                "ref": c_h_r.placename.ref
                            },
                        "relation":
                            {
                                "field": c_h_r.field,
                                "function": c_h_r.function,
                                "id": c_h_r.id
                            },
                        "role":
                            {
                                "description": c_h_r.placename_role.description,
                                "id": c_h_r.placename_role.id,
                                "label": c_h_r.placename_role.label
                            }
                    }
                    for c_h_r in self.obj.placenames_having_roles
                ],
            },
            "meta": self.meta,
            "links": {
                "self": self.self_link
            }
        }
        if self.with_relationships_links:
            resource["relationships"] = self.get_exposed_relationships()
        return resource

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
        resource = {
            **self.resource_identifier,
            "attributes": {
                "title": self.obj.title,
                "argument": self.obj.argument,
                "creation": self.obj.creation,
                #"creation-not-after": self.obj.creation_not_after,
                #"creation-label": self.obj.creation_label,
                "transcription": self.obj.transcription,
                "address": self.obj.address,
                "is-published": False if self.obj.is_published is None else self.obj.is_published,
                "witnesses": [{"id": w.id, "content": w.content, "classification-mark": w.classification_mark, "manifest_url": self.get_witness_manifest_url(w.id)} for w in sorted(self.obj.witnesses, key=lambda k: k.num) if self.obj.witnesses],
                "senders": [
                    {
                        "id": c_h_r.person.id,
                        "label": c_h_r.person.label,
                        "ref": c_h_r.person.ref
                    }
                    for c_h_r in self.obj.persons_having_roles if c_h_r.person_role.label == 'sender'
                ],
                "recipients": [
                    {
                        "id": c_h_r.person.id,
                        "label": c_h_r.person.label,
                        "ref": c_h_r.person.ref
                    }
                    for c_h_r in self.obj.persons_having_roles if c_h_r.person_role.label == 'recipient'
                ],
                "location_dates_from": [
                    {
                        "id": c_h_r.placename.id,
                        "label": c_h_r.placename.label,
                        "ref": c_h_r.placename.ref
                    }
                    for c_h_r in self.obj.placenames_having_roles if c_h_r.placename_role.label == 'location-date-from'
                ],
                "location_dates_to": [
                    {
                        "id": c_h_r.placename.id,
                        "label": c_h_r.placename.label,
                        "ref": c_h_r.placename.ref
                    }
                    for c_h_r in self.obj.placenames_having_roles if c_h_r.placename_role.label == 'location-date-to'
                ]
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

class DocumentLockFacade(DocumentFacade):
    def __init__(self, *args, **kwargs):
        super(DocumentLockFacade, self).__init__(*args, **kwargs)

    @property
    def resource(self):
        resource = {
            **self.resource_identifier,
            "attributes": {
                "is-published": False if self.obj.is_published is None else self.obj.is_published,
                "witnesses": [{"id": w.id, "content": w.content, "classification-mark": w.classification_mark,
                               "manifest_url": self.get_witness_manifest_url(w.id)} for w in self.obj.witnesses],
                "collections": [{'id': c.id, 'title': c.title} for c in self.obj.collections if self.obj.collections],
                "lock": [
                    {
                        "id": self.obj.locks[0].id,
                        "is_active": self.obj.locks[0].is_active,
                        "user_id": self.obj.locks[0].user.id,
                        "username": self.obj.locks[0].user.username,
                        "description": self.obj.locks[0].description,
                        "event_date": datetime_to_str(self.obj.locks[0].event_date),
                        "expiration_date": datetime_to_str(self.obj.locks[0].expiration_date),
                    }
                    if self.obj.locks else []]
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
