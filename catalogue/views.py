from flask import Blueprint, render_template

from .models import Category, Product

catalogue = Blueprint("catalogue", __name__)


@catalogue.route("/")
def index():
    return render_template('catalogue/index.html',
                           categories=Category.query.all(),
                           products=Product.query.all())
