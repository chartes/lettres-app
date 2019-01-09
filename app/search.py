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
            pprint.pprint(search)
            from collections import namedtuple
            Result = namedtuple("Result", "index id type score")

            results = [Result(str(hit['_index']),  str(hit['_id']), str(hit['_source']['type']), str(hit['_score']))
                       for hit in search['hits']['hits']]

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


from sqlalchemy import event, inspect

class ModelChangeEvent(object):
    def __init__(self, session, *callbacks):
        self.model_changes = {}
        self.callbacks = callbacks
        self.register_events(session)

    def record_ops(self, session, flush_context=None, instances=None):
        for targets, operation in ((session.new, 'insert'), (session.dirty, 'update'), (session.deleted, 'delete')):
            for target in targets:
                state = inspect(target)
                key = state.identity_key if state.has_identity else id(target)
                self.model_changes[key] = (target, operation)

    def after_commit(self, session):
        if self.model_changes:
            changes = list(self.model_changes.values())

            for callback in self.callbacks:
                callback(changes=changes)

            self.model_changes.clear()

    def after_rollback(self, session):
        self.model_changes.clear()

    def register_events(self, session):
        event.listen(session, 'before_flush', self.record_ops)
        event.listen(session, 'before_commit', self.record_ops)
        event.listen(session, 'after_commit', self.after_commit)
        event.listen(session, 'after_rollback', self.after_rollback)