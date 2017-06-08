import hashlib
from math import radians, sin, cos, atan2, sqrt

from flask import url_for
from flask_login import AnonymousUserMixin

from basket.models import Basket
from config import ShippingConfig
from database import db
from order.models import Discount


class User(db.Document):
    username = db.StringField(max_length=120, required=True)
    email = db.StringField(required=True)
    password = db.StringField(max_length=50)
    date_joined = db.DateTimeField()
    address = db.StringField(max_length=100, required=False)
    address_lat = db.FloatField(required=False)
    address_lng = db.FloatField(required=False)

    authenticated = db.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.set_password(self.password)
            self.id = str(self.id)
        super(User, self).save(*args, **kwargs)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return str(self.id)

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
        try:
            user_basket = Basket.objects.filter(is_submitted=False,
                                                user=self).first()
        except Basket.DoesNotExists:
            user_basket = Basket(user=self, is_submitted=False)
            user_basket.save()
        return user_basket

    @property
    def discount(self):
        return Discount.objects.active().filter(owner=self).first()

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
        return self.discounts.objects.active.exists()

    def generate_password(self, password):
        return hashlib.md5(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password == hashlib.md5(password.encode()).hexdigest()


class AnonymousUser(AnonymousUserMixin):
    pass
