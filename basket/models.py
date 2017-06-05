from decimal import Decimal

from catalogue.models import Product
from database import db
# from users.models import User


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
        # TODO: implement shipping price calculation
        return Decimal(30.00)  # for now

    @property
    def total_price_inc_discount(self):
        return self.total_price
        # user = User.query.get(self.user_id)
        # if not user.has_discount():
        #     return self.total_price
        #
        # discount = user.get_discount()
        #
        # if discount.in_percent:
        #     price = self.total_price * ((100 - discount.value) / 100)
        #     return price if price >= 0 else 0
        # else:
        #     price = self.total_price - discount.value
        #     return price if price >= 0 else 0

    @property
    def total_incl_discount_incl_shipping(self):
        return self.total_price_inc_discount + self.shipping_price

    def __str__(self):
        return 'Basket {}'.format(self.user.username)


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
