# importing libraries
from elasticsearch import Elasticsearch


def elasitcServerDashApp():
    lines = []
    with open("IP.txt") as f:
        lines = f.read().splitlines()
    es = Elasticsearch(
        hosts=[{"host": lines[0], "port": int(lines[1])}],
        refresh=True,
        use_ssl=False,
        retry_on_timeout=True,
    )
    return es
