from flask_script import Command
from pyelasticsearch import ElasticSearch

from catalogue.models import Product
from config import Config


class UpdateIndex(Command):
    def run(self):
        es = ElasticSearch(Config.ELASTICSEARCH_HOST)
        docs = [{'id': product.id, 'name': product.name} for product in
                Product.query.all()]
        es.bulk((es.index_op(doc, id=doc.pop('id')) for doc in docs),
                index='catalogue',
                doc_type='product')
        es.refresh('catalogue')
