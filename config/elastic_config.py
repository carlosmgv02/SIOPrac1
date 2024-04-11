from elasticsearch import Elasticsearch

from config.env_utils import get_env_value


def get_es_client():
    es = Elasticsearch(get_env_value('ELASTICSEARCH_URL'))
    return es
