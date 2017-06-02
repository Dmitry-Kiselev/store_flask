from flask import url_for
from flask_login import UserMixin, AnonymousUserMixin

from database import db
import datetime


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

    def __init__(self, username, email, password):
        super(User, self).__init__()
        self.username = username
        self.email = email
        self.password = password

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


class AnonymousUser(AnonymousUserMixin):
    pass
