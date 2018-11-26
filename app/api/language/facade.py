from app import db
from app.api.abstract_facade import JSONAPIAbstractFacade
from app.models import Language


class LanguageFacade(JSONAPIAbstractFacade):
    """

    """
    TYPE = "language"
    TYPE_PLURAL = "languages"

    @property
    def id(self):
        return self.obj.id

    @staticmethod
    def get_resource_facade(url_prefix, id, **kwargs):
        e = Language.query.filter(Language.id == id).first()
        if e is None:
            kwargs = {"status": 404}
            errors = [{"status": 404, "title": "language %s does not exist" % id}]
        else:
            e = LanguageFacade(url_prefix, e, **kwargs)
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
            co = Language(
                id=id,
                code=_g("code"),
                label=_g("label"),
            )
            db.session.add(co)
            db.session.commit()
            resource = co
        except Exception as e:
            print(e)
            errors = [{"status": 403, "title": "Error creating resource 'Language' with data: %s" % (
                str([id, attributes, related_resources]))}]
            db.session.rollback()
        return resource, errors

    def __init__(self, *args, **kwargs):
        super(LanguageFacade, self).__init__(*args, **kwargs)
        """Make a JSONAPI resource object describing what is a language
        """

        self.relationships = {

        }
        self.resource = {
            **self.resource_identifier,
            "attributes": {
                "id": self.obj.id,
                "name": self.obj.name,
                "ref": self.obj.ref
            },
            "meta": self.meta,
            "links": {
                "self": self.self_link
            }
        }

        if self.with_relationships_links:
            self.resource["relationships"] = self.get_exposed_relationships()
