from flask import Blueprint, render_template, flash, redirect, url_for
from flask import request
from flask.views import MethodView, View
from flask_login import current_user
from mongoengine.errors import DoesNotExist

from catalogue.models import Product
from .forms import LineForm
from .models import Line

basket = Blueprint("basket", __name__)


class IndexView(View):
    def get_lines(self):
        self.lines = current_user.get_basket.lines

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
        try:
            product = Product.objects.get(id=product_id)
        except DoesNotExist:
            return 404
        basket = current_user.get_basket
        if Line.objects.filter(product=product,
                               basket=basket).count():
            return redirect(url_for('catalogue.catalogue'))
        line = Line(product=product_id, basket=basket.id)
        line.save()
        flash('Added')
        return redirect(url_for('catalogue.catalogue'))


class UpdateLineQuantityView(MethodView):
    def post(self):
        try:
            line = Line.objects.get(id=request.form.get('line_id'))
        except DoesNotExist:
            return 404
        line.quantity = request.form.get('quantity')
        if line.quantity == '0':
            line.delete()
        else:
            line.save()
        return redirect(url_for('basket.basket_index'))


basket.add_url_rule("/",
                    view_func=IndexView.as_view('basket_index'))
basket.add_url_rule("/add/",
                    view_func=BasketAddView.as_view('basket_add'))
basket.add_url_rule("/update/",
                    view_func=UpdateLineQuantityView.as_view('update_line'))
