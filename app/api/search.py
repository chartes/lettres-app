import json

import elasticsearch
import pprint
from flask import current_app


class SearchIndexManager(object):
    #TODO Victor check if searchtype="fulltext" should be changed to "paratext" as default in backend
    @staticmethod
    def query_index(index, query, published=False, collectionsfacets=False, senders_facets=False, recipients_facets=False, persons_inlined_facets=False, location_dates_from_facets=False, location_dates_to_facets=False, locations_inlined_facets=False, ranges=(), groupby=None, sort_criteriae=None, searchtype=False, highlight=False, page=None, per_page=None, after=None):
        if not sort_criteriae:
            sort_criteriae = ["_score"]

        if groupby:
            searchtype = None
            highlight = False
        print('query_index searchtype row 18', searchtype, highlight)

        if not query:
            #if search is without a searched string, than match all, regardless of search type (API, frontend searches)
            print('\nquery_index NO QUERY STRING / searchtype, highlight :\n', searchtype, highlight)
            body_query = {
                "bool": {
                    "must": [{
                        "match_all": {}
                    }]
                }
            }
            body_highlight = {
            }
            print('\nquery_index NO QUERY STRING / body_query, body_highlight :\n', body_query, body_highlight)
        else:
            #if search has a searched string, check where to match the searched string based on search type (frontend fulltext or paratext or else)
            if searchtype == "fulltext":
                #fulltext is always provided with a query from the front-end
                #if searchtype is fulltext, we search only in fields transcription & address
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
                #if searchtype is paratext, we search only in fields title & argument
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
            else:
                #if no frontend types (fulltext or paratext) is provided, we do not return highlights by default
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

        body_aggregations = {}
        if searchtype:
            #for frontend searches on /search, searchtype is either fulltext/paratext and response require facets, obtained via aggregations
            body_aggregations = {
                    "collections": {
                        "terms": {
                            "field": "collections.id",
                            "size": 100000
                        },
                    },
                    "senders": {
                        "terms": {
                            "field": "senders.facet_key",
                            "size": 100000
                        }
                    },
                    "recipients": {
                        "terms": {
                            "field": "recipients.facet_key",
                            "size": 100000
                        }
                    },
                    "persons_inlined": {
                        "terms": {
                            "field": "persons_inlined.facet_key",
                            "size": 100000
                        }
                    },
                    "location_dates_from": {
                        "terms": {
                            "field": "location_dates_from.facet_key",
                            "size": 100000
                        }
                    },
                    "location_dates_to": {
                        "terms": {
                            "field": "location_dates_to.facet_key",
                            "size": 100000
                        }
                    },
                    "locations_inlined": {
                        "terms": {
                            "field": "locations_inlined.facet_key",
                            "size": 100000
                        }
                    }
            }


        if hasattr(current_app, 'elasticsearch'):
            #start building ES query body
            body = {
                "query": body_query,
                "aggregations": body_aggregations,
                "highlight": body_highlight,
                "sort": [
                    #  {"creation": {"order": "desc"}}
                    *sort_criteriae
                ],
                "track_scores": True,
                "track_total_hits": True,
            }
            #check for additionnal filters and facets
            print("\npublished check : \n", published)
            if published:
                body["query"]["bool"]["must"].append({"term": {"is-published": True}})

            if collectionsfacets:
                if len(json.loads(collectionsfacets)["collections"]) > 0:
                    print("\nlen(json.loads(collectionsfacets)['collections']) :\n", len(json.loads(collectionsfacets)["collections"]))
                    body["query"]["bool"]["must"].append({"terms": {f"collections.id": json.loads(collectionsfacets)["collections"]}})

            if senders_facets:
                body["query"]["bool"]["must"].append({"term": {"senders.facet_key": senders_facets}})

            if recipients_facets:
                for recipient in recipients_facets:
                    body["query"]["bool"]["must"].append({"term": {"recipients.facet_key": recipient}})

            if persons_inlined_facets:
                for person in persons_inlined_facets:
                    body["query"]["bool"]["must"].append({"term": {"persons_inlined.facet_key": person}})

            if location_dates_from_facets:
                body["query"]["bool"]["must"].append({"term": {"location_dates_from.facet_key": location_dates_from_facets}})

            if location_dates_to_facets:
                for location_to in location_dates_to_facets:
                    body["query"]["bool"]["must"].append({"term": {"location_dates_to.facet_key": location_to}})

            if locations_inlined_facets:
                for location_inlined in locations_inlined_facets:
                    body["query"]["bool"]["must"].append({"term": {"locations_inlined.facet_key": location_inlined}})

            print("\nfacets checks : \n", body["query"])

            if len(ranges) > 0:
                for range in ranges:
                    range["creation_range"]["format"] = "yyyy"
                    #print("\nranges : \n", ranges)
                    #print("\nbody['query'] before ranges : \n", body["query"])
                    #body["query"]["bool"]["filter"] = {"range": range} filter also works but may clash with already defined filters
                    body["query"]["bool"]["must"].append({"range": range})

                    print("\nbody['query'] after ranges : \n ", body["query"])

            if highlight:
                #for API usage, allow getting highlights on transcription & address only
                print('\nif highlight / query : ', query, '\ngroupby : ', groupby, '\nhighlight : ', highlight)
                body["highlight"] = {
                    "type": "fvh",
                    "fields": {
                        #"argument": {},
                        #"title": {},
                        "transcription": {},
                        "address": {}
                    },
                    "number_of_fragments": 100,
                    "options": {"return_offsets": False}
                }
                print('\nif highlight / body["highlight"] : ', body["highlight"], '\n')

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

            #finalise building ES query body
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

            #check index and launch ES search
            try:
                if index is None or len(index) == 0:
                    index = current_app.config["DEFAULT_INDEX_NAME"]
                print("\nindex : ", index, "\nbody : \n")
                pprint.pprint(body)
                search = current_app.elasticsearch.search(index=index, body=body)
                # from elasticsearch import Elasticsearch
                # scan = Elasticsearch.helpers.scan(client=current_app.elasticsearch, index=index, body=body)

                from collections import namedtuple
                results = []
                if searchtype or highlight:
                    Result = namedtuple("Result", "index id type score highlight")
                    #print("search['hits']['total'] : ", search['hits']['total'])
                    if search['hits']['total']['value'] > 0:
                        for hit in search['hits']['hits']:
                            results = [Result(str(hit['_index']), str(hit['_id']), str(hit['_source']["type"]),
                                              str(hit['_score']), hit.get('highlight'))
                                       for hit in search['hits']['hits']]

                    print('\nsearch.py query_index results searchtype or highlights : \n', results[0] if len(results) > 0 else "No result")
                else:
                    Result = namedtuple("Result", "index id type score")

                    results = [Result(str(hit['_index']), str(hit['_id']), str(hit['_source']["type"]),
                                      str(hit['_score']))
                               for hit in search['hits']['hits']]
                    print('\nsearch.py query_index results no highlights : \n', results[0] if len(results) > 0 else "No result")

                buckets = []
                after_key = None
                count = search['hits']['total']['value']

                # print(body, len(results), search['hits']['total'], index)
                #pprint.pprint(search)
                if not groupby and 'aggregations' in search:
                    buckets = {}
                    for key, value in search["aggregations"].items():
                        facette = value["buckets"] if "buckets" in value else []
                        buckets[key] = facette

                    if "senders" in buckets and senders_facets:
                        buckets["senders"] = [x for x in buckets["senders"] if x["key"] != senders_facets]
                    if "recipients" in buckets and recipients_facets:
                        buckets["recipients"] = [x for x in buckets["recipients"] if x["key"] not in recipients_facets]
                    if "persons_inlined" in buckets and persons_inlined_facets:
                        buckets["persons_inlined"] = [x for x in buckets["persons_inlined"] if x["key"] not in persons_inlined_facets]

                    if "location_dates_from" in buckets and location_dates_from_facets:
                        buckets["location_dates_from"] = [x for x in buckets["location_dates_from"] if x["key"] != location_dates_from_facets]
                    if "location_dates_to" in buckets and location_dates_to_facets:
                        buckets["location_dates_to"] = [x for x in buckets["location_dates_to"] if x["key"] not in location_dates_to_facets]
                    if "locations_inlined" in buckets and locations_inlined_facets:
                        buckets["locations_inlined"] = [x for x in buckets["locations_inlined"] if x["key"] not in locations_inlined_facets]

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
        current_app.elasticsearch.index(index=index, id=id, body=payload)

    @staticmethod
    def remove_from_index(index, id):
        # print("REMOVE_FROM_INDEX", index, id)
        try:
            current_app.elasticsearch.delete(index=index,  id=id)
        except elasticsearch.exceptions.NotFoundError as e:
            print("WARNING: resource already removed from index:", str(e))
