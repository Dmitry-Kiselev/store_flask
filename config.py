import os

from decimal import Decimal

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '2sXBwWL5CeyG6ZcFBCe92zrb2LGetNwQ'
    SQLALCHEMY_DATABASE_URI = "postgresql://store:store@localhost/store"


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class PaymentConfig:
    PAYMENT_SERVICE = 'stripe'
    STRIPE_API_KEY = 'sk_test_kdrKohTAdfuCZgqCRO8ctkzL'


class ShippingConfig:
    free_shipping_on = Decimal(10000)
    fixed_shipping_price = Decimal(30)
    shipping_price_per_km = Decimal(1.5)

    address_lat = 47.8356042
    address_lng = 35.1219634
