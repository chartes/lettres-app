import elasticsearch
import pprint
from flask import current_app


class SearchIndexManager(object):

    @staticmethod
    def query_index(index, query, ranges=(), groupby=None, sort_criteriae=None, searchtype="fulltext", aggregated_test=False, highlight=False, page=None, per_page=None, after=None):
        if sort_criteriae is None:
            sort_criteriae = []

        if aggregated_test:
            if hasattr(current_app, 'elasticsearch'):
                body = {
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "query_string": {
                                        "query": query,
                                        "default_operator": "AND",

                                    },
                                }
                            ]
                        },
                    },
                    "aggregations": {
                        "collection": {
                            "terms": {
                                "field": "collections.title.keyword",
                            },
                        },
                        "sender": {
                            "terms": {
                                "field": "senders.label.keyword"
                            }
                        },
                        "recipient": {
                            "terms": {
                                "field": "recipients.label.keyword"
                            }
                        },
                        "person-inlined": {
                            "terms": {
                                "field": "person-inlined.label.keyword"
                            }
                        },
                        "location-date-from": {
                            "terms": {
                                "field": "location-date-from.label.keyword"
                            }
                        },
                        "location-date-to": {
                            "terms": {
                                "field": "location-date-to.label.keyword"
                            }
                        },
                        "location-inlined": {
                            "terms": {
                                "field": "location-inlined.label.keyword"
                            }
                        }
                    },
                    "sort": [
                        #  {"creation": {"order": "desc"}}
                        *sort_criteriae
                    ],
                    "track_scores": True
                }

                if len(ranges) > 0:
                    for range in ranges:
                        body["query"]["bool"]["must"].append({"range": range})

                if highlight:
                    print('for query : ', query, groupby, ', highlight : ', highlight)
                    body["highlight"] = {
                        "type": "fvh",
                        "fields": {
                            "transcription": {}
                        },
                        "number_of_fragments": 100,
                        "options": {"return_offsets": False}
                    }
                    print('\nbody["highlight"] : ', body["highlight"], '\n')
                body["size"] = 0

                if groupby is not None:
                    '''body["aggregations"] = {
                        "items": {
                            "composite": {
                                "sources": [
                                    {
                                        "item": {
                                            "terms": {
                                                "field": groupby,
                                            },
                                        }
                                    },
                                ],
                                "size": per_page
                            }
                        },
                        "type_count": {
                            "cardinality": {
                                "field": "id"
                            }
                        },
                        "bucket_count": {
                            "cardinality": {
                                "field": groupby
                            },
                        },
                    }'''
                    body["size"] = 0

                    sort_criteriae.reverse()
                    '''for crit in sort_criteriae:
                        for crit_name, crit_order in crit.items():
                            body["aggregations"]["items"]["composite"]["sources"].insert(0,
                                                                                         {
                                                                                             crit_name: {
                                                                                                 "terms": {
                                                                                                     "field": crit_name,
                                                                                                     **crit_order},
                                                                                             }
                                                                                         }
                                                                                         )
                    
                    if after is not None:
                        sources_keys = [list(s.keys())[0] for s in
                                        body["aggregations"]["items"]["composite"]["sources"]]
                        body["aggregations"]["items"]["composite"]["after"] = {key: value for key, value in
                                                                               zip(sources_keys, after.split(','))}
                        # print(sources_keys, after, {key: value for key, value in zip(sources_keys, after.split(','))})
                    '''
                if per_page is not None:
                    if page is None or groupby is not None:
                        page = 0
                    else:
                        page = page - 1  # is it correct ?
                    body["from"] = page * per_page
                    body["size"] = per_page
                else:
                    body["from"] = 0 * per_page
                    body["size"] = per_page
                    # print("WARNING: /!\ for debug purposes the query size is limited to", body["size"])
                try:
                    if index is None or len(index) == 0:
                        index = current_app.config["DEFAULT_INDEX_NAME"]

                    # pprint.pprint(body)
                    search = current_app.elasticsearch.search(index=index, doc_type="_doc", body=body)
                    # from elasticsearch import Elasticsearch
                    # scan = Elasticsearch.helpers.scan(client=current_app.elasticsearch, index=index, doc_type="_doc", body=body)
                    #for hit in search['hits']['hits']:

                    if highlight:
                        results = [{
                            'score': hit['_score'],
                            'type': hit['_source']["type"],
                            'id': int(hit['_id']),
                            'published': hit['_source']['is-published'],
                            'creation' : str(hit['_source']['creation']),
                            'title': hit['_source']['title'],
                            'argument': hit['_source']['argument'],
                            'address': hit['_source']['address'],
                            'transcription': ({ "raw": hit['_source']['transcription'], "highlight": hit['highlight']['transcription']} if 'highlight' in hit.keys() else { "raw": hit['_source']['transcription']}) ,
                            'collections': hit['_source']['collections'],
                            'senders': hit['_source']['senders'],
                            'recipients': hit['_source']['recipients'],
                            'origins': hit['_source']['location-date-from'],
                            'destinations': hit['_source']['location-date-to']
                        } for hit in search['hits']['hits']]

                    else:
                        results = [{
                            'score': hit['_score'],
                            'type': hit['_source']["type"],
                            'id': int(hit['_id']),
                            'published': hit['_source']['is-published'],
                            'creation' : str(hit['_source']['creation']),
                            'title': hit['_source']['title'],
                            'argument': hit['_source']['argument'],
                            'address': hit['_source']['address'],
                            'transcription': hit['_source']['transcription'],
                            'collections': hit['_source']['collections'],
                            'senders': hit['_source']['senders'],
                            'recipients': hit['_source']['recipients'],
                            'origins': hit['_source']['location-date-from'],
                            'destinations': hit['_source']['location-date-to']
                        } for hit in search['hits']['hits']]
                    search['hits']['hits'] = results

                    '''from collections import namedtuple
                    results = []
                    if highlight:
                        Result = namedtuple("Result", "index id type score highlight")
                        # print("search['hits']['total'] : ", search['hits']['total'])
                        if search['hits']['total'] > 0:
                            for hit in search['hits']['hits']:
                                results = [Result(str(hit['_index']), str(hit['_id']), str(hit['_source']["type"]),
                                                  str(hit['_score']), hit.get('highlight'))
                                           for hit in search['hits']['hits']]

                        print('results : ', results)
                    else:
                        print('tada')
                        Result = namedtuple("Result", "index id type score")

                        results = [Result(str(hit['_index']), str(hit['_id']), str(hit['_source']["type"]),
                                          str(hit['_score']))
                                   for hit in search['hits']['hits']]
                    search['results'] = results
                    
                    #buckets = []
                    after_key = None
                    count = search['hits']['total']

                    # print(body, len(results), search['hits']['total'], index)
                    # pprint.pprint(search)
                    if 'aggregations' in search:
                        buckets = search["aggregations"]["items"]["buckets"]

                        # grab the after_key returned by ES for future queries
                        if "after_key" in search["aggregations"]["items"]:
                            after_key = search["aggregations"]["items"]["after_key"]
                        # print("aggregations: {0} buckets; after_key: {1}".format(len(buckets), after_key))
                        # pprint.pprint(buckets)
                        count = search["aggregations"]["type_count"]["value"]
                        return results, buckets, after_key, count
                    else:
                        return results, buckets, after_key, count
                    '''
                    return search
                except Exception as e:
                    print('query_index error')
                    raise e

        if groupby:
            highlight = False
        #highlight = type(highlight) == str
        print('query_index highlight row 245', highlight)

        if not searchtype:
            searchtype = "fulltext"

        if searchtype  == "fulltext":
            body_query = {
                    "bool": {
                        "must": [
                            {
                                "query_string": {
                                    "query": query,
                                    "default_operator": "AND",
                                    "fields": ["transcription", "address"]
                                }
                            }
                        ]
                    },
                }
            body_highlight = {
                    "type": "fvh",
                    "fields": {
                        "address": {},
                        "transcription": {}
                    },
                    "number_of_fragments": 100,
                    "options": {"return_offsets": False}
                }
        elif searchtype == "paratext":
            body_query = {
                    "bool": {
                        "must": [
                            {
                                "query_string": {
                                    "query": query,
                                    "default_operator": "AND",
                                    "fields": ["title", "argument"]
                                }
                            }
                        ]
                    },
                }
            body_highlight = {
                "type": "fvh",
                "fields": {
                    "argument": {},
                },
                "number_of_fragments": 100,
                "options": {"return_offsets": False}
            }
        if hasattr(current_app, 'elasticsearch'):
            body = {
                "query": body_query,
                "aggregations": {

                },
                "highlight": body_highlight,
                "sort": [
                    #  {"creation": {"order": "desc"}}
                    *sort_criteriae
                ],
                "track_scores": True
            }

            if len(ranges) > 0:
                for range in ranges:
                    body["query"]["bool"]["must"].append({"range": range})

            '''if highlight:
                print('for query : ',query, groupby,', highlight : ', highlight)
                body["highlight"] = {
                    "type": "fvh",
                    "fields": {
                        "argument": {},
                        "title": {},
                        "transcription": {}
                    },
                    "number_of_fragments": 100,
                    "options": {"return_offsets": False}
                }
                print('\nbody["highlight"] : ', body["highlight"],'\n')'''

            if groupby is not None:
                body["aggregations"] = {
                    "items": {
                        "composite": {
                            "sources": [
                                {
                                    "item": {
                                        "terms": {
                                            "field": groupby,
                                        },
                                    }
                                },
                            ],
                            "size": per_page
                        }
                    },
                    "type_count": {
                        "cardinality": {
                            "field": "id"
                        }
                    },
                    "bucket_count": {
                        "cardinality": {
                            "field": groupby
                        },
                    },
                }
                body["size"] = 0

                sort_criteriae.reverse()
                for crit in sort_criteriae:
                    for crit_name, crit_order in crit.items():
                        body["aggregations"]["items"]["composite"]["sources"].insert(0,
                                                                                     {
                                                                                         crit_name: {
                                                                                             "terms": {
                                                                                                 "field": crit_name,
                                                                                                 **crit_order},
                                                                                         }
                                                                                     }
                                                                                     )

                if after is not None:
                    sources_keys = [list(s.keys())[0] for s in body["aggregations"]["items"]["composite"]["sources"]]
                    body["aggregations"]["items"]["composite"]["after"] = {key: value for key, value in
                                                                           zip(sources_keys, after.split(','))}
                    #print(sources_keys, after, {key: value for key, value in zip(sources_keys, after.split(','))})

            if per_page is not None:
                if page is None or groupby is not None:
                    page = 0
                else:
                    page = page - 1  # is it correct ?
                body["from"] = page * per_page
                body["size"] = per_page
            else:
                body["from"] = 0 * per_page
                body["size"] = per_page
                # print("WARNING: /!\ for debug purposes the query size is limited to", body["size"])
            try:
                if index is None or len(index) == 0:
                    index = current_app.config["DEFAULT_INDEX_NAME"]
                print("\nboby : \n")
                pprint.pprint(body)
                search = current_app.elasticsearch.search(index=index, doc_type="_doc", body=body)
                # from elasticsearch import Elasticsearch
                # scan = Elasticsearch.helpers.scan(client=current_app.elasticsearch, index=index, doc_type="_doc", body=body)

                from collections import namedtuple
                results = []
                if highlight:
                    Result = namedtuple("Result", "index id type score highlight")
                    #print("search['hits']['total'] : ", search['hits']['total'])
                    if search['hits']['total'] > 0:
                        for hit in search['hits']['hits']:
                            results = [Result(str(hit['_index']), str(hit['_id']), str(hit['_source']["type"]),
                                              str(hit['_score']), hit.get('highlight'))
                                       for hit in search['hits']['hits']]

                    #print('results : ',results)
                else:
                    Result = namedtuple("Result", "index id type score")

                    results = [Result(str(hit['_index']), str(hit['_id']), str(hit['_source']["type"]),
                                      str(hit['_score']))
                               for hit in search['hits']['hits']]
                    print('results : ', results)

                buckets = []
                after_key = None
                count = search['hits']['total']

                # print(body, len(results), search['hits']['total'], index)
                # pprint.pprint(search)
                if 'aggregations' in search:
                    buckets = search["aggregations"]["items"]["buckets"]

                    # grab the after_key returned by ES for future queries
                    if "after_key" in search["aggregations"]["items"]:
                        after_key = search["aggregations"]["items"]["after_key"]
                    #print("aggregations: {0} buckets; after_key: {1}".format(len(buckets), after_key))
                    # pprint.pprint(buckets)
                    count = search["aggregations"]["type_count"]["value"]
                    return results, buckets, after_key, count
                else:
                    return results, buckets, after_key, count

            except Exception as e:
                print('query_index error')
                raise e

    @staticmethod
    def add_to_index(index, id, payload):
        # print("ADD_TO_INDEX", index, id)
        current_app.elasticsearch.index(index=index, doc_type="_doc", id=id, body=payload)

    @staticmethod
    def remove_from_index(index, id):
        # print("REMOVE_FROM_INDEX", index, id)
        try:
            current_app.elasticsearch.delete(index=index, doc_type="_doc", id=id)
        except elasticsearch.exceptions.NotFoundError as e:
            print("WARNING: resource already removed from index:", str(e))
