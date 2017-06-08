import datetime
from decimal import Decimal

from mongoengine import QuerySet

from database import db


class Order(db.Document):
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

    basket = db.ReferenceField('Basket')
    status = db.IntField(choices=ORDER_STATUS.STATUS_CHOICES,
                         default=ORDER_STATUS.PENDING)
    discount = db.ReferenceField('Basket', required=False)

    @property
    def total_price(self):
        shipping_price = self.basket.shipping_price
        if not self.discount:
            return self.basket.total_price + Decimal(shipping_price)

        if self.discount.in_percent:
            return self.basket.total_price * (
                (100 - self.discount.value) / 100) + shipping_price
        else:
            return self.basket.total_price - self.discount.value + Decimal(
                shipping_price)

    @property
    def get_discount_val(self):
        if not self.discount:
            return 0
        if self.discount.in_percent:
            return self.basket.total_price - (
                self.basket.total_price * Decimal(
                    (100 - self.discount.value) / 100))
        else:
            return self.basket.total_price - (
                self.basket.total_price - self.discount.value)

    def get_status(self):
        return dict(Order.ORDER_STATUS.STATUS_CHOICES)[self.status]


class DiscountQuerySet(QuerySet):
    def active(self):
        now = datetime.datetime.now()
        return self.filter(
            available_from__lte=now, available_until__gte=now)


class Discount(db.Document):
    meta = {'queryset_class': DiscountQuerySet}

    owner = db.ReferenceField('User')
    value = db.DecimalField()
    in_percent = db.BooleanField(default=False)
    available_from = db.DateTimeField()
    available_until = db.DateTimeField()

    def mark_as_used(self):
        self.is_used = True
