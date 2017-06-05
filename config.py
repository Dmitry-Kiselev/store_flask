import os

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