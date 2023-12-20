import datetime

from app import db
from app.api.abstract_facade import JSONAPIAbstractFacade
from app.api.witness.facade import WitnessFacade
from app.models import Lock, datetime_to_str


class LockFacade(JSONAPIAbstractFacade):
    """

    """
    TYPE = "lock"
    TYPE_PLURAL = "locks"

    MODEL = Lock

    @property
    def id(self):
        return self.obj.id

    def to_document_es_part(self):
        return self.obj.to_document_es_part()

    #@staticmethod
    #def get_resource_facade(url_prefix, id, **kwargs):
    #    e = Lock.query.filter(Lock.id == id).first()
    #    if e is None:
    #        kwargs = {"status": 404}
    #        errors = [{"status": 404, "title": "lock %s does not exist" % id}]
    #    else:
    #        e = LockFacade(url_prefix, e, **kwargs)
    #        kwargs = {}
    #        errors = []
    #    return e, kwargs, errors

    def get_witness_manifest_url(self, id):
        w = [x for x in self.obj.documents.witnesses if x.id == id]
        if len(w) == 0:
            return None
        # do not return a manifest if it has no images
        canvas_ids = [img.canvas_id for img in w[0].images]
        if len(canvas_ids) == 0:
            return None
        f_obj, errors, kwargs = WitnessFacade.get_facade('', w[0])
        return f_obj.get_iiif_manifest_url()

    @property
    def resource(self):
        resource = {
            **self.resource_identifier,
            "attributes": {
                "object-id": self.obj.object_id,
                "object-type": self.obj.object_type,

                "event-date": datetime_to_str(self.obj.event_date),
                "expiration-date": datetime_to_str(self.obj.expiration_date),
                "is-active": self.obj.is_active,
                "description": self.obj.description,
                "collections": [{'id': c.id, 'title': c.title} for c in self.obj.documents.collections if self.obj.documents.collections],
                "witnesses": [{"id": w.id, "content": w.content, "manifest_url": self.get_witness_manifest_url(w.id)} for w in self.obj.documents.witnesses if self.obj.documents.witnesses]
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
        super(LockFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is a lock
        """
        from app.api.user.facade import UserFacade
        from app.api.document.facade import DocumentFacade

        self.relationships = {
            "user": {
                "links": self._get_links(rel_name="user"),
                "resource_identifier_getter": self.get_related_resource_identifiers(UserFacade, "user"),
                "resource_getter": self.get_related_resources(UserFacade, "user"),
            },
            "documents": {
                "links": self._get_links(rel_name="documents"),
                "resource_identifier_getter": self.get_related_resource_identifiers(DocumentFacade, "documents",
                                                                                    to_many=False),
                "resource_getter": self.get_related_resources(DocumentFacade, "documents", to_many=False),
            }

        }
        '''self.relationships.update({
            "documents": {
                "links": self._get_links(rel_name="documents"),
                "resource_identifier_getter": self.get_related_resource_identifiers(DocumentFacade, "documents", to_many=False),
                "resource_getter": self.get_related_resources(DocumentFacade, "documents", to_many=False),
            }
        })'''
    def get_data_to_index_when_added(self, propagate):
        _res = self.resource
        payload = self.to_document_es_part()
        latest_lock_data = [{"id": _res["id"], "index": self.get_index_name(), "payload": payload}]
        if not propagate:
            return
        else:
            return latest_lock_data + self.get_relationship_data_to_index(rel_name="documents")

    def reindex(self, op, propagate=True):
        if op == "update":
            print("reindex update")
            # Updates of collection metadata shouldn't impact linked documents
            self.add_to_index(True)
        else:
            print("reindex not update")
            super().reindex(op, propagate)


    '''@staticmethod
    def update_resource(obj, obj_type, related_resources, append=False):
        print("lock update_resource obj, obj_type, related_ressources", obj, obj_type, related_resources)
        latest_lock = obj
        if latest_lock.event_date is None:
            latest_lock.event_date = datetime.datetime.now()
            latest_lock.expiration_date = datetime.datetime.now()
            related_resources.event_date = latest_lock.event_date
            related_resources.expiration_date = latest_lock.expiration_date
        #latest_lock = Lock.query.filter(Lock.id == obj.id).first()
        print("\nupdate_resource latest_lock ", latest_lock)

        from app.api.document.facade import DocumentFacade
        document = obj.documents
        print("lock update_resource doc, obj", document, obj)
        DocumentFacade.update_resource(
            document,
            "document",
            attributes={},
            related_resources={"lock": latest_lock}
        )
        DocumentFacade("", document).reindex("update", propagate=True)
        attributes = {}
        return JSONAPIAbstractFacade.update_resource(
            latest_lock,
            obj_type,
            attributes,
            related_resources
        )'''