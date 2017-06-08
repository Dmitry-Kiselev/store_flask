from decimal import Decimal

from flask_login import current_user

from config import ShippingConfig
from database import db


class Basket(db.Document):
    user = db.ReferenceField("User")
    is_submitted = db.BooleanField()

    @property
    def lines(self):
        return Line.objects.filter(basket=self)

    @property
    def total_price(self):
        return sum([line.line_price for line in self.lines])

    @property
    def lines_count(self):
        return self.lines.objects.count()

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


class Line(db.Document):
    product = db.ReferenceField("Product")
    quantity = db.IntField(default=1)
    basket = db.ReferenceField("Basket")

    @property
    def line_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return '{} {}'.format(self.product.name, self.quantity)

# @event.listens_for(Line, 'after_delete')
# @event.listens_for(Line, 'after_insert')
# def update_cache(mapper, connection, target):
#     key = current_user.get_basket.id
#     count = Line.query.filter(Line.basket_id == key).count()
#     cache.set('basket_{}'.format(key), count, None)
