from database import db


class Basket(db.Model):
    __tablename__ = "baskets"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_submitted = db.Column(db.Boolean())
    lines = db.relationship("Line", backref='line', lazy='dynamic')

    @property
    def total_price(self):
        return sum([line.line_price for line in self.lines.all()])

    def __str__(self):
        return 'Basket {}'.format(self.user.username)


class Line(db.Model):
    __tablename__ = "lines"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer())
    basket_id = db.Column(db.Integer, db.ForeignKey('baskets.id'))

    @property
    def line_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return '{} {}'.format(self.product.name, self.quantity)
