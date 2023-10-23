import json

import elasticsearch
import pprint
from flask import current_app


class SearchIndexManager(object):

    @staticmethod
    def query_index(index, query, published=False, personsfacets=False, placesfacets=False, ranges=(), groupby=None, sort_criteriae=None, searchtype=False, highlight=False, page=None, per_page=None, after=None):
        if sort_criteriae is None:
            sort_criteriae = []

        if groupby:
            searchtype = None
            highlight = False
        #highlight = type(highlight) == str
        print('query_index searchtype row 245', searchtype, highlight)
        if query.startswith("*"):
            print('query.startswith("*")', searchtype, highlight)
            searchtype = False
            body_query = {
                  "bool": {
                     "must": [
                         {
                             "query_string": {
                                 "query": query,
                                 "default_operator": "AND",
                             }
                         }
                     ]
                  }
            }
            body_highlight = {
            }

        else:
            if not searchtype:
                searchtype = "fulltext"
            if searchtype  == "fulltext" and query !="*":
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
            elif searchtype == "paratext" and query !="*":
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
        body_aggregations = {}
        if not groupby:
            body_aggregations = {
                    "collections": {
                        "terms": {
                            "field": "collections.title.keyword",
                            "size": 100000
                        },
                    },
                    "persons": {
                        "terms": {
                            "field": "persons.label.keyword",
                            "size": 100000
                        }
                    },
                    "senders": {
                        "terms": {
                            "field": "senders.label.keyword",
                            "size": 100000
                        }
                    },
                    "recipients": {
                        "terms": {
                            "field": "recipients.label.keyword",
                            "size": 100000
                        }
                    },
                    "persons_inlined": {
                        "terms": {
                            "field": "persons_inlined.label.keyword",
                            "size": 100000
                        }
                    },
                    "location_dates_from": {
                        "terms": {
                            "field": "location_dates_from.label.keyword",
                            "size": 100000
                        }
                    },
                    "location_dates_to": {
                        "terms": {
                            "field": "location_dates_to.label.keyword",
                            "size": 100000
                        }
                    },
                    "locations_inlined": {
                        "terms": {
                            "field": "locations_inlined.label.keyword",
                            "size": 100000
                        }
                    }
            }


        if hasattr(current_app, 'elasticsearch'):
            body = {
                "query": body_query,
                "aggregations": body_aggregations,
                "highlight": body_highlight,
                "sort": [
                    #  {"creation": {"order": "desc"}}
                    *sort_criteriae
                ],
                "track_scores": True
            }
            print("\npublished check : \n", published)
            if published:
                body["query"]["bool"]["must"].append({"term": {"is-published": True}})

            if personsfacets:
                for facet_name, facets in json.loads(personsfacets).items():
                    if len(facets) > 0:
                        for person in facets:
                            body["query"]["bool"]["must"].append({"term": {f"{facet_name}.label.keyword": person}})

            if placesfacets:
                for facet_name, facets in json.loads(placesfacets).items():
                    if len(facets) > 0:
                        for place in facets:
                            body["query"]["bool"]["must"].append({"term": {f"{facet_name}.label.keyword": place}})
            print("\nfacets checks : \n", body["query"])

            if len(ranges) > 0:
                for range in ranges:
                    print("\nranges : ", ranges)
                    body["query"]["bool"]["must"].append({"range": range})
                    print("\nbody['query'] \n : ", body["query"])

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
                    #print('results : ', results)

                buckets = []
                after_key = None
                count = search['hits']['total']

                # print(body, len(results), search['hits']['total'], index)
                #pprint.pprint(search)
                if not groupby and 'aggregations' in search:
                    buckets = {}
                    for key, value in search["aggregations"].items():
                        facette = [v for k, v in value.items() if k == 'buckets'][0]
                        buckets[key] = facette
                    #buckets = search["aggregations"]
                    return results, buckets, after_key, count
                elif groupby and 'aggregations' in search:
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
