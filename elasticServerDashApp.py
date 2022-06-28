# importing libraries
from elasticsearch import Elasticsearch


def elasitcServerDashApp():
    es = Elasticsearch(["http://127.0.0.1:9200"], refresh=True, use_ssl=False)
    return es
