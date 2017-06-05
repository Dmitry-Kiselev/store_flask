from flask import Blueprint, render_template, flash, redirect, url_for
from flask import request
from flask.views import MethodView
from flask_login import current_user

from database import db
from .models import Line

basket = Blueprint("basket", __name__)


def index():
    return render_template('basket/basket.html',
                           lines=current_user.get_basket.lines.all())


class BasketAddView(MethodView):
    def post(self):
        product_id = request.form.get('id')
        basket = current_user.get_basket
        if not product_id:
            return 403
        line = Line(product_id=product_id, basket_id=basket.id)
        db.session.add(line)
        db.session.commit()
        flash('Added')
        return redirect(url_for('catalogue.catalogue'))


basket.add_url_rule("/", 'basket_index',
                    view_func=index)
basket.add_url_rule("/add/",
                    view_func=BasketAddView.as_view('basket_add'))
