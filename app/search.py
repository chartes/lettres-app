import pprint
from flask import current_app

from app import db


def query_index(index, query, fields=None, page=None, per_page=None):
    if hasattr(current_app, 'elasticsearch'):
        body = {
            'query': {
                'query_string': {
                    'query': query,
                    #'fields': ['collections'] if fields is None or len(fields) == 0 else fields
                }
            },
        }

        if per_page is not None:
            if page is None:
                page = 0
            else:
                page = page - 1  # is it correct ?
            body["from"] = page * per_page
            body["size"] = per_page
        else:
            body["from"] = 0 * per_page
            body["size"] = per_page
            #print("WARNING: /!\ for debug purposes the query size is limited to", body["size"])

        try:
            search = current_app.elasticsearch.search(index=index, doc_type=index, body=body)
            from collections import namedtuple
            Result = namedtuple("Result", "index id type score")

            results = [Result(str(hit['_index']),  str(hit['_id']), str(hit['_source']['type']), str(hit['_score']))
                       for hit in search['hits']['hits']]

            print(search)
            print(len(results), search['hits']['total'], index, body)

            return results, search['hits']['total']

        except Exception as e:
            print(e)
            return [], 0


class SearchableMixin(object):

    @classmethod
    def search(cls, expression, fields=None, page=None, per_page=None, index=None):
        if index is None:
            raise ValueError

        # perform the query
        print(page, per_page)
        results, total = query_index(index=index, query=expression,
                                     fields=fields, page=page, per_page=per_page)
        print(expression, results, total)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        ids = [r.id for r in results]

        if len(ids) == 0:
            return cls.query.filter_by(id=0), 0

        for i in range(len(ids)):
            when.append((ids[i], i))

        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        #session._changes = {
        #    'add': list(session.new),
        #    'update': list(session.dirty),
        #    'delete': list(session.deleted)
        #}
        from app.api.facade_manager import JSONAPIFacadeManager
        session._changes = {"add": {}, "remove": {}}

        # get id and payload info for each new or dirty object :
        for new_obj in list(session.new) + list(session.dirty):
            if isinstance(new_obj, SearchableMixin):
                facade = JSONAPIFacadeManager.get_facade_class(new_obj)
                f_obj, kwargs, errors = facade.get_facade("", new_obj)
                index_name = f_obj.get_index_name()
                # register the change to the index
                if index_name:
                    if index_name not in session._changes["add"]:
                        session._changes["add"][index_name] = []
                    data_to_index = f_obj.get_indexed_data()
                    if data_to_index:
                        session._changes["add"][index_name].append({"src_obj": new_obj, "payload": data_to_index})

        for new_obj in list(session.deleted):
            if isinstance(new_obj, SearchableMixin):
                facade = JSONAPIFacadeManager.get_facade_class(new_obj)
                f_obj, kwargs, errors = facade.get_facade("", new_obj)
                index_name = f_obj.get_index_name()
                # register the change to the index
                if index_name:
                    if index_name not in session._changes["remove"]:
                        session._changes["remove"][index_name] = []
                    session._changes["remove"][index_name].append({"src_obj": new_obj})
    @classmethod
    def after_commit(cls, session):
        for index in session._changes['add'].keys():
            for p in session._changes['add'][index]:
                p["payload"]["id"] = p["src_obj"].id
                #pprint.pprint(p)
                cls.add_to_index(index, p["src_obj"].id, p["payload"])

        for index in session._changes['remove'].keys():
            for p in session._changes['remove'][index]:
                cls.remove_from_index(index, p["src_obj"].id)
        session._changes = None

    @classmethod
    def add_to_index(cls, index, id, payload):
        current_app.elasticsearch.index(index=index, doc_type=index, id=id, body=payload)

    @classmethod
    def remove_from_index(cls, index, id):
        current_app.elasticsearch.delete(index=index, doc_type=index, id=id)

    @classmethod
    def reindex(cls):
        if hasattr(current_app, 'elasticsearch'):
            from app.api.facade_manager import JSONAPIFacadeManager
            for obj in cls.query:
                facade = JSONAPIFacadeManager.get_facade_class(obj)
                f_obj, kwargs, errors = facade.get_facade("", obj)
                data_to_index = f_obj.get_indexed_data()
                if data_to_index:
                    index_name = f_obj.get_index_name()
                    print("+ indexing", obj)
                    cls.add_to_index(index_name, obj.id, data_to_index)

