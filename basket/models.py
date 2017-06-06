from decimal import Decimal

from flask_login import current_user
from sqlalchemy import event

from catalogue.models import Product
from config import ShippingConfig
from database import db
from extensions import cache


class Basket(db.Model):
    __tablename__ = "baskets"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_submitted = db.Column(db.Boolean())
    lines = db.relationship("Line", backref='line', lazy='dynamic')

    @property
    def total_price(self):
        return sum([line.line_price for line in self.lines.all()])

    @property
    def lines_count(self):
        return self.lines.count()

    def submit(self):
        self.is_submitted = True

    @property
    def shipping_price(self):
        if self.total_price_inc_discount > ShippingConfig.free_shipping_on:
            return 0  # free shipping

        distance = current_user.distance
        if distance is None:
            return ShippingConfig.fixed_shipping_price  # fixed price

        return Decimal(distance) * ShippingConfig.shipping_price_per_km

    @property
    def total_price_inc_discount(self):
        if not current_user.has_discount():
            return self.total_price

        discount = current_user.discount

        if discount.in_percent:
            price = self.total_price * ((100 - discount.value) / 100)
            return price if price >= 0 else 0
        else:
            price = self.total_price - discount.value
            return price if price >= 0 else 0

    @property
    def total_incl_discount_incl_shipping(self):
        return self.total_price_inc_discount + self.shipping_price

    def __str__(self):
        return 'Basket {}'.format(self.id)


class Line(db.Model):
    __tablename__ = "lines"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer(), default=1)
    basket_id = db.Column(db.Integer, db.ForeignKey('baskets.id'))

    @property
    def line_price(self):
        return self.product.price * self.quantity

    @property
    def product(self):
        return Product.query.get(self.product_id)

    def __str__(self):
        return '{} {}'.format(self.product.name, self.quantity)


@event.listens_for(Line, 'after_delete')
@event.listens_for(Line, 'after_insert')
def update_cache(mapper, connection, target):
    key = current_user.get_basket.id
    count = Line.query.filter(Line.basket_id == key).count()
    cache.set('basket_{}'.format(key), count, None)
