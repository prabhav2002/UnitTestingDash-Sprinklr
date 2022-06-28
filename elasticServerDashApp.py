# importing libraries
from elasticsearch import Elasticsearch


def elasitcServerDashApp():
    lines = []
    with open("IP.txt") as f:
        lines = f.readlines()
    es = Elasticsearch(
        hosts=[{"host": lines[0]}],
        refresh=True,
        use_ssl=False,
        retry_on_timeout=True,
    )
    return es
