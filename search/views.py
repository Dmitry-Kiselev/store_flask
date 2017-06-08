from flask import render_template, request, Blueprint
from flask.views import View
from pyelasticsearch import ElasticSearch

from catalogue.models import Product
from config import Config

search = Blueprint("search", __name__)


class SearchView(View):
    def dispatch_request(self):
        es = ElasticSearch(Config.ELASTICSEARCH_HOST)
        q = request.args['q']
        result = es.search('name:{}'.format(q), index='catalogue')
        num_results = result['hits']['total']
        product_ids = [hit['_id'] for hit in result['hits']['hits']]
        products = Product.objects.filter(id__in=product_ids)
        return render_template('search/search.html', num_results=num_results,
                               products=products, q=q)


search.add_url_rule("/",
                    view_func=SearchView.as_view('search'))
