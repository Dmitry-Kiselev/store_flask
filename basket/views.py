from flask import Blueprint, render_template
from flask_login import current_user

from catalogue.models import Category, Product
from .models import Basket, Line

basket = Blueprint("basket", __name__)


@basket.route("/")
def index():
    return render_template('basket/basket.html',
                           lines=current_user.get_basket.lines.all())