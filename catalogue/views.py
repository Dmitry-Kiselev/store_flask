from flask import Blueprint, render_template

from .models import Category, Product

catalogue = Blueprint("catalogue", __name__)


@catalogue.route("/")
def index():
    return render_template('catalogue/index.html',
                           categories=Category.query.all(),
                           products=Product.query.all())


@catalogue.route("catalogue/")
def catalogue_view():
    return render_template('catalogue/catalogue.html',
                           products=Product.query.all())


@catalogue.route("catalogue/<product_id>/")
def product_detail(product_id):
    return render_template('catalogue/product_detail.html',
                           product=Product.query.get(product_id))
