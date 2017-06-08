from database import db
from order.models import Order


class Payment(db.Document):
    charge_id = db.StringField(max_length=120, unique=True, required=True)
    charged_sum = db.DecimalField()
    discount_sum = db.DecimalField()
    order = db.ReferenceField("Order")

    def __init__(self, *args, **kwargs):
        super(Payment, self).__init__(*args, **kwargs)

        if self.order:
            self.charged_sum = self.order.total_price
            self.discount_sum = self.order.get_discount_val
            if self.charge_id:
                self.order.status = Order.ORDER_STATUS.PROCESSING
                self.order.save()

    def __str__(self):
        return '{}'.format(self.charge_id)
