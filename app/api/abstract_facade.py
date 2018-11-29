from app import db
from app.models import SearchableMixin


class JSONAPIAbstractFacade(object):

    """

    """
    TYPE = "ABSTRACT-TYPE"
    TYPE_PLURAL = "ABSTRACT-TYPE-PLURAL"

    ITEMS_PER_PAGE = 10000 #TODO: au delà il faut passer par l'api scroll d'elastic search

    def __init__(self, url_prefix, obj, with_relationships_links=True, with_relationships_data=True):
        self.obj = obj
        self.url_prefix = url_prefix
        self.with_relationships_data = with_relationships_data
        self.with_relationships_links = with_relationships_links

        self.self_link = "{url_prefix}/{type_plural}/{id}".format(
            url_prefix=self.url_prefix, type_plural=self.TYPE_PLURAL, id=self.id
        )

        self.resource_identifier = {
            "type": self.TYPE,
            "id": self.id
        }

        self._links_template = {
            "self": "{url_prefix}/{source_col}/{source_id}/relationships".format(
                    url_prefix=self.url_prefix, source_col=self.TYPE_PLURAL, source_id=self.id
            ),
            "related": "{url_prefix}/{source_col}/{source_id}".format(
                    url_prefix=self.url_prefix, source_col=self.TYPE_PLURAL, source_id=self.id
            )
        }

        self.relationships = {}

    @property
    def id(self):
        raise NotImplementedError

    @property
    def resource(self):
        raise NotImplementedError

    @property
    def search_fields(self):
        if isinstance(self.obj, SearchableMixin):
            return self.obj.__searchable__
        else:
            return []

    @property
    def meta(self):
        return {}

    @staticmethod
    def make_resource_identifier(id, type):
        return {"id": id, "type": type}

    @staticmethod
    def get_resource_facade(*args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def post_resource(model, obj_id, attributes, related_resources):
        """
        Instantiate the obj but do not commit it
        :param model:
        :param obj_id:
        :param attributes:
        :param related_resources:
        :return:
        """
        print("CREATING RESOURCE:", obj_id, attributes, related_resources)

        for att in attributes.keys():
            attributes[att.replace("-", "_")] = attributes.pop(att)

        attributes["id"] = obj_id
        print("  setting attributes", attributes)
        resource = model(**attributes)

        # set related resources
        for rel_name, rel_data in related_resources.items():
            rel_name = rel_name.replace("-", "_")
            print("  setting", rel_name, rel_data)
            if hasattr(resource, rel_name):
                try:
                    setattr(resource, rel_name, rel_data)
                except Exception:
                    setattr(resource, rel_name, rel_data[0])

        return resource

    @staticmethod
    def create_resource(model, obj_id, attributes, related_resources):
        errors = None
        resource = None
        try:
            resource = JSONAPIAbstractFacade.post_resource(model, obj_id, attributes, related_resources)
            db.session.add(resource)
            db.session.commit()
        except Exception as e:
            print(e)
            errors = {
                "status": 403,
                "title": "Error creating resource with data: %s" % str([attributes, related_resources]),
                "detail": str(e)
            }
            db.session.rollback()
        return resource, errors

    # noinspection PyArgumentList
    @staticmethod
    def patch_resource(obj, obj_type, attributes, related_resources, append):
        """
        Update the obj but do not commit it
        :param append:
        :param obj:
        :param obj_type:
        :param attributes:
        :param related_resources:
        :return:
        """
        print("UPDATING RESOURCE:", obj, obj_type, attributes, related_resources)
        # update attributes
        for att, att_value in attributes.items():
            att_name = att.replace("-", "_")
            print("  setting", att, att_value)
            if hasattr(obj, att_name):
                setattr(obj, att_name, att_value)
            else:
                raise AttributeError("Attribute %s does not exist" % att_name)

        # update related resources
        for rel_name, rel_data in related_resources.items():
            rel_name = rel_name.replace("-", "_")
            print("  setting", rel_name, rel_data)
            if hasattr(obj, rel_name):
                # append (POST) or replace (PATCH) replace related resources ?
                if not append:
                    try:
                        setattr(obj, rel_name, rel_data)
                    except Exception:
                        setattr(obj, rel_name, rel_data[0])
                else:
                    try:
                        setattr(obj, rel_name, getattr(obj, rel_name, []) + rel_data)
                    except Exception:
                        setattr(obj, rel_name, getattr(obj, rel_name, []) + rel_data[0])
            else:
                raise AttributeError("Relationship %s does not exist" % rel_name)
        return obj

    @staticmethod
    def update_resource(obj, obj_type, attributes, related_resources, append=False):
        errors = None
        resource = None
        try:
            resource = JSONAPIAbstractFacade.patch_resource(obj, obj_type, attributes, related_resources, append)
            db.session.add(resource)
            db.session.commit()
        except Exception as e:
            print(e)
            errors = {
                "status": 403,
                "title": "Error updating resource '%s' with data: %s" % (
                    obj_type, str([id, attributes, related_resources, append])),
                "detail": str(e)
            }
            db.session.rollback()
        return resource, errors

    @staticmethod
    def delete_resource():
        raise NotImplementedError

    def set_relationships_mode(self, w_rel_links, w_rel_data):
        self.with_relationships_links = w_rel_links
        self.with_relationships_data = w_rel_data

    def _get_links(self, rel_name):
        return {
            "self": "{template}/{rel_name}".format(template=self._links_template["self"], rel_name=rel_name),
            "related": "{template}/{rel_name}".format(template=self._links_template["related"], rel_name=rel_name)
        }

    def get_exposed_relationships(self):
        if self.with_relationships_data:
            return {
                rel_name: {
                    "links": rel["links"],
                    "data": rel["resource_identifier_getter"]()
                }
                for rel_name, rel in self.relationships.items()
            }
        else:
            # do not provide relationship data, provide just the links
            return {
                rel_name: {
                    "links": rel["links"],
                }
                for rel_name, rel in self.relationships.items()
            }