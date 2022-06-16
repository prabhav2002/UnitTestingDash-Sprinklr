# importing libraries
from elasticsearch import Elasticsearch


def elasitcServerDashApp():
    es = Elasticsearch(refresh="true")
    return es
