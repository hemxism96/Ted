from elasticsearch import Elasticsearch
import json
from app import db

class initialize_es(){

    es= Elasticsearch()

    with open('mapping.json','r') as f:
        mapping = json.load(f)

    es.indices.create(index='search', body=mapping)

    data=db.find({})

    es.index(index='search', doc_type='_doc', body=data)

}