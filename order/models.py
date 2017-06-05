import datetime
from decimal import Decimal

from sqlalchemy_utils.types.choice import ChoiceType

from basket.models import Basket
from database import db


class Order(db.Model):
    class ORDER_STATUS:
        PENDING = 0
        FAILED = 1
        PROCESSING = 2
        COMPLETED = 3

        STATUS_CHOICES = (
            (PENDING, 'Pending payment'),
            (FAILED, 'Failed'),
            (PROCESSING, 'Processing'),
            (COMPLETED, 'Completed')
        )

    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    basket_id = db.Column(db.Integer, db.ForeignKey('baskets.id'))
    status = db.Column(db.SmallInteger, ChoiceType(ORDER_STATUS.STATUS_CHOICES),
                       default=ORDER_STATUS.PENDING)
    discount_id = db.Column(db.Integer, db.ForeignKey('discounts.id'),
                            nullable=True)

    def __init__(self, basket_id, discount_id):
        self.basket_id = basket_id
        self.discount_id = discount_id

    @property
    def total_price(self):
        basket = Basket.query.get(self.basket_id)
        shipping_price = basket.shipping_price
        if not self.discount_id:
            return basket.total_price + Decimal(shipping_price)
        discount = Discount.query.get(self.discount_id)

        if discount.in_percent:
            return basket.total_price * (
                (100 - discount.value) / 100) + shipping_price
        else:
            return basket.total_price - discount.value + Decimal(shipping_price)

    @property
    def get_discount_val(self):
        if not self.discount_id:
            return 0
        discount = Discount.query.get(self.discount_id)
        basket = Basket.query.get(self.basket_id)
        if discount.in_percent:
            return basket.total_price - (
                basket.total_price * Decimal((100 - discount.value) / 100))
        else:
            return basket.total_price - (
                basket.total_price - discount.value)

    def get_status(self):
        return dict(Order.ORDER_STATUS.STATUS_CHOICES)[self.status]


class Discount(db.Model):
    __tablename__ = "discounts"
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    value = db.Column(db.DECIMAL)
    in_percent = db.Column(db.Boolean, default=False)
    available_from = db.Column(db.DateTime)
    available_until = db.Column(db.DateTime)

    def is_active(self):
        now = datetime.datetime.now()
        return self.available_from <= now and self.available_until >= now

    def mark_as_used(self):
        self.is_used = True
