from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from catalogue.models import Product, Category
from database import db
from users.models import User


def configure_admin_views(app):
    admin = Admin(app, name='Store', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Product, db.session))
    admin.add_view(ModelView(Category, db.session))
