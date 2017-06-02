from flask import url_for
from sqlalchemy_mptt.mixins import BaseNestedSets

from database import db


class TimeStampedModel(db.Model):
    __abstract__ = True

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(),
                           onupdate=db.func.now())


class Category(TimeStampedModel, BaseNestedSets):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(400), index=True, unique=True)
    items = db.relationship("Product", backref='item', lazy='dynamic')

    def __str__(self):
        return '<Category {}>'.format(self.name)


class Product(TimeStampedModel):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    name = db.Column(db.String(475), index=True)
    description = db.Column(db.Text(), nullable=True)
    price = db.Column(db.DECIMAL())
    num_in_stock = db.Column(db.DECIMAL())

    def get_absolute_url(self):
        return url_for('catalogue.product_detail', product_id=self.id)

    def __str__(self):
        return '<Product {}>'.format(self.name)


class ProductRating(TimeStampedModel):
    __tablename__ = 'product_ratings'
    id = db.Column(db.Integer, primary_key=True)
    rated_product = db.ForeignKey('Product')
    user = db.ForeignKey('User')
    rating = db.SmallInteger()
