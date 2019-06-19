#!/usr/bin/env python
import sys
import json
import hysds.celery
import requests


def query(tsid):
    '''
    Queries for the given product to get index and type
    @param tsid: id to query for
    '''
    es_url = hysds.celery.app.conf.GRQ_ES_URL
    es_index = "grq"
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "term": {
                            "_id": tsid
                        }
                    },
                ]
            }
        }
    }
    url = "%s/%s/_search/" % (es_url, es_index)
    data = json.dumps(query, indent=2)
    print("Posting ES search: {0} with {1}".format(url, data))
    r = requests.post(url, data=data)
    r.raise_for_status()
    print("Got: {0}".format(r.json()))
    result = r.json()
    if len(result["hits"]["hits"]) == 0:
        raise Exception("Interferogram not found in ES index: {0}".format(tsid))
    elif len(result["hits"]["hits"]) > 1:
        raise Exception("Interferogram found multiple times: {0}".format(tsid))
    return (es_url, result["hits"]["hits"][0]["_index"],
            result["hits"]["hits"][0]["_type"])


def update(lf_url, tsid):
    '''
    '''
    # get dataset id
    if '/' in tsid: tsid = tsid.split('/')[0]
    url, index, tpe = query(tsid)
    new_doc = {"doc": {"visualization-url": lf_url}, "doc_as_upsert": True}
    url = "{0}/{1}/{2}/{3}/_update".format(url, index, tpe, tsid)
    print("Updating: {0} with {1}".format(url, new_doc))
    r = requests.post(url, data=json.dumps(new_doc))
    r.raise_for_status()


if __name__ == "__main__":
    '''
    Main program
    '''
    if len(sys.argv) != 3:
        print("Not enough arguments: leaflet-url and time series id required")
        sys.exit(1)
    update(sys.argv[1], sys.argv[2])
