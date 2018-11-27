from app import db
from app.api.abstract_facade import JSONAPIAbstractFacade
from app.models import Note


class NoteFacade(JSONAPIAbstractFacade):
    """

    """
    TYPE = "note"
    TYPE_PLURAL = "notes"

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def get_resource_facade(url_prefix, id, **kwargs):
        e = Note.query.filter(Note.id == id).first()
        if e is None:
            kwargs = {"status": 404}
            errors = [{"status": 404, "title": "note %s does not exist" % id}]
        else:
            e = NoteFacade(url_prefix, e, **kwargs)
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
            co = Note(
                id=id,
                content=_g("content"),
                label=_g("label"),
                document_id=_g("document-id"),
            )
            db.session.add(co)
            db.session.commit()
            resource = co
        except Exception as e:
            print(e)
            errors = [{"status": 403, "title": "Error creating resource 'Note' with data: %s" % (str([id, attributes, related_resources]))}]
            db.session.rollback()
        return resource, errors

    def __init__(self, *args, **kwargs):
        super(NoteFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is an note
        """

        self.relationships = {

        }
        self.resource = {
            **self.resource_identifier,
            "attributes": {
                "id": self.obj.id,
                "label": self.obj.label,
                "content": self.obj.content,
                "document-id": self.obj.document_id
            },
            "meta": self.meta,
            "links": {
                "self": self.self_link
            }
        }

        if self.with_relationships_links:
            self.resource["relationships"] = self.get_exposed_relationships()
