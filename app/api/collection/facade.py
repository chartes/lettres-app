from flask import current_app

from app.api.abstract_facade import JSONAPIAbstractChangeloggedFacade
from app.api.user.facade import UserFacade
from app.api.document.facade import DocumentFacade
from app.models import Collection, User


class CollectionFacade(JSONAPIAbstractChangeloggedFacade):
    """

    """
    TYPE = "collection"
    TYPE_PLURAL = "collections"

    MODEL = Collection

    @property
    def id(self):
        return self.obj.id

    #@staticmethod
    #def get_resource_facade(url_prefix, id, **kwargs):
    #    e = Collection.query.filter(Collection.id == id).first()
    #    if e is None:
    #        kwargs = {"status": 404}
    #        errors = [{"status": 404, "title": "Collection %s does not exist" % id}]
    #    else:
    #        e = CollectionFacade(url_prefix, e, **kwargs)
    #        kwargs = {}
    #        errors = []
    #    return e, kwargs, errors

    def get_parents_resource_identifiers(self, rel_facade=None):
        parents = self.obj.parents
        rel_facade = CollectionFacade if not rel_facade else rel_facade

        return [] if parents is None else [
            rel_facade.make_resource_identifier(parent.id, rel_facade.TYPE)
            for parent in parents
        ]

    def get_children_resource_identifiers(self, rel_facade=None):
        children = self.obj.children
        rel_facade = CollectionFacade if not rel_facade else rel_facade

        return [] if children is None else [
            rel_facade.make_resource_identifier(child.id, rel_facade.TYPE)
            for child in children
        ]

    def get_parents_resources(self, rel_facade=None):
        parents = self.obj.parents
        rel_facade = CollectionFacade if not rel_facade else rel_facade

        return [] if parents is None else [
            rel_facade(self.url_prefix, parent, self.with_relationships_links,
                       self.with_relationships_data).resource
            for parent in parents
        ]

    def get_children_resources(self, rel_facade=None):
        children = self.obj.children
        rel_facade = CollectionFacade if not rel_facade else rel_facade

        return [] if children is None else [
            rel_facade(self.url_prefix, child, self.with_relationships_links,
                       self.with_relationships_data).resource
            for child in children
        ]

    @property
    def resource(self):
        if not self.obj.documents_including_children:
            date_min = None
            date_max = date_min
        else:
            creation = [
                doc.creation for doc in self.obj.documents_including_children
                if doc.creation
            ]
            date_min = min(creation)
            date_max = max(creation)

        resource = {
            **self.resource_identifier,
            "attributes": {
                "title": self.obj.title,
                "path": [c.title for c in self.obj.parents] + [self.obj.title],
                "description": self.obj.description,
                "nb_docs": len(self.obj.documents_including_children),
                "date_min": date_min,
                "date_max": date_max
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
        super(CollectionFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is a Collection
        """

        from app.api.document.facade import DocumentFacade

        self.relationships.update({
            "documents": {
                "links": self._get_links(rel_name="documents"),
                "resource_identifier_getter": self.get_related_resource_identifiers(DocumentFacade, "documents", to_many=True),
                "resource_getter": self.get_related_resources(DocumentFacade, "documents", to_many=True),
            },
            "documents-including-children": {
                "links": self._get_links(rel_name="documents-including-children"),
                "resource_identifier_getter": self.get_related_resource_identifiers(DocumentFacade, "documents_including_children",
                                                                                    to_many=True),
                "resource_getter": self.get_related_resources(DocumentFacade, "documents_including_children", to_many=True),
            },
            "admin": {
                "links": self._get_links(rel_name="admin"),
                "resource_identifier_getter": self.get_related_resource_identifiers(UserFacade, "admin", to_many=False),
                "resource_getter": self.get_related_resources(UserFacade, "admin", to_many=False),
            },
            "parents": {
                "links": self._get_links(rel_name="parents"),
                "resource_identifier_getter": self.get_parents_resource_identifiers,
                "resource_getter": self.get_parents_resources,
            },
            "children": {
                "links": self._get_links(rel_name="children"),
                "resource_identifier_getter": self.get_children_resource_identifiers,
                "resource_getter": self.get_children_resources,
            }
        })

    def get_data_to_index_when_added(self, propagate):
        _res = self.resource
        payload = {
            "id": _res["id"],
            "type": _res["type"],

            "title": _res["attributes"]["title"],
            "description": _res["attributes"]["description"],
        }
        collection_data = [{"id": _res["id"], "index": self.get_index_name(), "payload": payload}]
        if not propagate:
            return collection_data
        else:
            return collection_data + self.get_relationship_data_to_index(rel_name="documents")

    def remove_from_index(self, propagate):
        from app.api.search import SearchIndexManager
        SearchIndexManager.remove_from_index(index=self.get_index_name(), id=self.id)

        if propagate:
            # reindex the docs without the resource
            for data in self.get_data_to_index_when_added(propagate):
                if data["payload"]["id"] != self.id and data["payload"]["type"] != self.TYPE:
                    data["payload"]["collections"] = [l for l in data["payload"]["collections"] if l.get("id") != self.id]
                    SearchIndexManager.add_to_index(index=data["index"], id=data["id"], payload=data["payload"])

    @staticmethod
    def delete_resource(obj):
        default_col_title = current_app.config["UNSORTED_DOCUMENTS_COLLECTION_TITLE"]
        if obj.title == default_col_title:
            error = {
                "status": 400,
                "title": f"Unsorted documents collection '{default_col_title}' cannot be deleted"
            }
            print(error)
            return error
        collections_to_remove = [obj, *obj.children_including_children]
        # if collection has parent collection, move documents there
        if obj.parent_id:
            new_collection = Collection.query.get(obj.parent_id)
        # if not, move documents to unsorted documents collection
        else:
            new_collection = Collection.query.filter(
                Collection.title == default_col_title
            ).first()
        # move all documents (including documents in subcollections) to new collection
        documents = obj.documents_including_children
        for document in documents:
            collections = [
                col for col in document.collections
                if col not in collections_to_remove
            ]
            # only add to unsorted documents collection
            # if document is not related to any other
            if not collections or new_collection.title != default_col_title:
                collections.append(new_collection)
            DocumentFacade.update_resource(
                document,
                "document",
                attributes={},
                related_resources={"collections": collections}
            )
            DocumentFacade("", document).reindex("update", propagate=True)
        # delete all collections
        # remove child collections before parent collections
        collections_to_remove.sort(key=lambda c: c.id, reverse=True)
        for collection in collections_to_remove:
            errors = JSONAPIAbstractChangeloggedFacade.delete_resource(
                collection
            )
            if errors:  # stop if any collection cannot be removed
                return errors
        return errors

    def _validate_resource(attributes):
        # validate admin_id
        admin_id = attributes.get("admin_id")
        if not admin_id:
            return {
                "status": 400,
                "title": "Attribute 'admin_id' is missing",
            }
        user = User.query.filter(User.id == admin_id).first()
        if not user:
            return {
                "status": 400,
                "title": f"No user with ID '{admin_id}'"
            }
        if not user.is_admin():
            return {
                "status": 400,
                "title": f"User with ID '{user.id}' is not admin",
            }
        # validate title
        title = attributes.get("title")
        if not title:
            return {
                "status": 400,
                "title": "Attribute 'title' is missing or empty"
            }
        return None

    @staticmethod
    def create_resource(model, obj_id, attributes, related_resources):
        error = CollectionFacade._validate_resource(attributes)
        if error:
            print(error["title"])
            return None, error
        resource, error = JSONAPIAbstractChangeloggedFacade.create_resource(
            model,
            obj_id,
            attributes,
            related_resources
        )
        # UNIQUE constraint failed
        if error and error["status"] == 409:
            return resource, {
                "status": 409,
                "title": f"Invalid data (Hint: check if title '{attributes['title']}' is already in use)",    # noqa
            }
        return resource, error

    @staticmethod
    def update_resource(obj, obj_type, attributes, related_resources, append=False):
        error = CollectionFacade._validate_resource(attributes)
        if error:
            print(error["title"])
            return None, error
        return JSONAPIAbstractChangeloggedFacade.update_resource(
            obj,
            obj_type,
            attributes,
            related_resources,
            append=append
        )


class CollectionHierarchyOnlyFacade(CollectionFacade):
    TYPE = "collection"
    TYPE_PLURAL = "collections"

    MODEL = Collection

    def __init__(self, *args, **kwargs):
        super(CollectionHierarchyOnlyFacade, self).__init__(*args, **kwargs)
        self.relationships = {
            "admin": self.relationships['admin'],
            "parents": self.relationships["parents"],
            "children": self.relationships["children"]
        }
