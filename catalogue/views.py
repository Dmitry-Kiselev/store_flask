from flask import Blueprint, render_template

from extensions import cache
from .models import Category, Product

catalogue = Blueprint("catalogue", __name__)


@cache.cached(timeout=50)
def index():
    return render_template('catalogue/index.html',
                           categories=Category.objects.all(),
                           products=Product.objects.all())


@cache.cached(timeout=50)
def catalogue_view():
    return render_template('catalogue/catalogue.html',
                           products=Product.objects.all())


@cache.cached(timeout=50)
def product_detail(product_id):
    return render_template('catalogue/product_detail.html',
                           product=Product.objects.get(id=product_id))


catalogue.add_url_rule('/', 'index', index)
catalogue.add_url_rule('catalogue/', 'catalogue', catalogue_view)
catalogue.add_url_rule('catalogue/<product_id>/', 'product_detail',
                       product_detail)
