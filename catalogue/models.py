import datetime

from flask import url_for

from database import db


class TimeStampedModel(db.Document):
    meta = {
        'abstract': True,
    }

    created_on = db.DateTimeField()
    updated_on = db.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.created_on:
            self.created_on = datetime.datetime.now()
        self.updated_on = datetime.datetime.now()
        return super(TimeStampedModel, self).save(*args, **kwargs)


class Category(TimeStampedModel):
    name = db.StringField(max_length=120, required=True)
    parent = db.ReferenceField("Category", required=False)
    left = db.ReferenceField("Category", required=False)
    right = db.ReferenceField("Category", required=False)
    products = db.ReferenceField("Discount", required=False)

    def __str__(self):
        return '<Category {}>'.format(self.name)


class Product(TimeStampedModel):
    category = db.ReferenceField("Category", required=True)
    name = db.StringField(max_length=120, required=True)
    description = db.StringField(max_length=120, required=False)
    price = db.DecimalField()
    num_in_stock = db.IntField()

    def get_absolute_url(self):
        return url_for('catalogue.product_detail', product_id=self.id)

    def __str__(self):
        return '<Product {}>'.format(self.name)
