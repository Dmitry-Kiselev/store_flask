from flask import Blueprint, render_template, flash, redirect, url_for
from flask import request
from flask.views import MethodView, View
from flask_login import current_user
from sqlalchemy.sql import exists

from database import db
from .forms import LineForm
from .models import Line, Basket

basket = Blueprint("basket", __name__)


class IndexView(View):
    def get_lines(self):
        self.lines = current_user.get_basket.lines.all()

    def get_forms(self):
        self.forms = [LineForm(
            quantity=line.quantity, line_id=line.id)
            for line in self.lines]

    def dispatch_request(self):
        self.get_lines()
        self.get_forms()
        return render_template('basket/basket.html',
                               lines=self.lines, forms=self.forms)


class BasketAddView(MethodView):
    def post(self):
        product_id = request.form.get('id')
        basket = current_user.get_basket
        if not product_id:
            return 403
        if db.session.query(exists().where(Line.product_id == product_id).where(
                        Basket.id == basket.id)).scalar():
            return redirect(url_for('catalogue.catalogue'))
        line = Line(product_id=product_id, basket_id=basket.id)
        db.session.add(line)
        db.session.commit()
        flash('Added')
        return redirect(url_for('catalogue.catalogue'))


class UpdateLineQuantityView(MethodView):
    def post(self):
        print(request.form)
        line = Line.query.get(request.form.get('line_id'))
        line.quantity = request.form.get('quantity')
        if line.quantity == 0:
            db.session.delete(line)
        db.session.commit()
        return redirect(url_for('basket.basket_index'))


basket.add_url_rule("/",
                    view_func=IndexView.as_view('basket_index'))
basket.add_url_rule("/add/",
                    view_func=BasketAddView.as_view('basket_add'))
basket.add_url_rule("/update/",
                    view_func=UpdateLineQuantityView.as_view('update_line'))
