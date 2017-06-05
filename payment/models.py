from database import db
from order.models import Order


class Payment(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.Integer, primary_key=True)
    charge_id = db.Column(db.String(200), unique=True, nullable=False)
    charged_sum = db.Column(db.DECIMAL)
    discount_sum = db.Column(db.DECIMAL)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))

    def __init__(self, *args, **kwargs):
        super(Payment, self).__init__(*args, **kwargs)
        self.charge_id = kwargs.get('charge_id')
        self.order_id = kwargs.get('order_id')

        if self.order_id:
            order = Order.query.get(self.order_id)
            self.charged_sum = order.total_price
            self.discount_sum = order.get_discount_val
            if self.charge_id:
                order.status = Order.ORDER_STATUS.PROCESSING
                db.session.commit()

    def __str__(self):
        return '{}'.format(self.charge_id)
