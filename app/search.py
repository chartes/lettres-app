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
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                cls.add_to_index(obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                cls.add_to_index(obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                cls.remove_from_index(obj)
        session._changes = None

    @classmethod
    def add_to_index(cls, obj):
        if hasattr(current_app, 'elasticsearch'):
            from app.api.facade_manager import JSONAPIFacadeManager
            facade = JSONAPIFacadeManager.get_facade_class(obj)
            f_obj, kwargs, errors = facade.get_facade("", obj)
            data_to_index = f_obj.indexed_data
            #if data_to_index:
            #    index_name = f_obj.get_index_name()
            #    current_app.elasticsearch.index(index=index_name, doc_type=index_name, id=obj.id,
            #                                    body=data_to_index)

    @classmethod
    def remove_from_index(cls, obj):
        if hasattr(current_app, 'elasticsearch'):
            from app.api.facade_manager import JSONAPIFacadeManager
            facade = JSONAPIFacadeManager.get_facade_class(obj)
            index_name = facade.get_index_name()
            current_app.elasticsearch.delete(index=index_name, doc_type=index_name, id=obj.id)

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            cls.add_to_index(obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)