import datetime
import hashlib
from math import radians, sin, cos, atan2, sqrt

from flask import url_for
from flask_login import UserMixin, AnonymousUserMixin

from basket.models import Basket
from config import ShippingConfig
from database import db
from order.models import Discount


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column('password', db.String(120), nullable=False)
    date_joined = db.Column(db.DateTime(timezone=True),
                            default=datetime.datetime.now,
                            nullable=False)
    address = db.Column(db.String(100), nullable=True)
    address_lat = db.Column(db.Float, nullable=True)
    address_lng = db.Column(db.Float, nullable=True)

    authenticated = db.Column(db.Boolean, default=False)

    basket = db.relationship("Basket", backref='basket', lazy='dynamic')
    discounts = db.relationship("Discount", backref='discount', lazy='dynamic')

    def __init__(self, username, email, password):
        super(User, self).__init__()
        self.username = username
        self.email = email
        self.password = self.set_password(password)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    @property
    def url(self):
        """Returns the url for the user."""
        return url_for("user.profile", username=self.username)

    def __str__(self):
        return "<{} {}>".format(self.__class__.__name__, self.username)

    @property
    def get_basket(self):
        user_basket = self.basket.filter_by(is_submitted=False).first()
        if not user_basket:
            user_basket = Basket(user_id=self.id, is_submitted=False)
            db.session.add(user_basket)
            db.session.commit()
        return user_basket

    @property
    def discount(self):
        active_discounts = [x for x in
                            self.discounts if
                            x.is_active()]
        if active_discounts:
            return active_discounts[0]
        return None

    @property
    def distance(self):
        company_lat, company_lng = ShippingConfig.address_lat, ShippingConfig.address_lng
        user_lat, user_lng = self.address_lat, self.address_lng

        if not (company_lat and company_lng and user_lat and user_lng):
            return None

        # approximate radius of earth in km
        R = 6373.0

        lat1 = radians(company_lat)
        lon1 = radians(company_lng)
        lat2 = radians(user_lat)
        lon2 = radians(user_lng)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        return distance

    def has_discount(self):
        now = datetime.datetime.now()
        return Discount.query.filter(Discount.available_from <= now,
                                     Discount.available_until >= now).count()

    def set_password(self, password):
        self.password = hashlib.md5(password.encode())

    def check_password(self, password):
        return self.password == hashlib.md5(password.encode())


class AnonymousUser(AnonymousUserMixin):
    pass
