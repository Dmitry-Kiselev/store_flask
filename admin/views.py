from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView

from basket.models import Basket, Line
from catalogue.models import Product, Category, ProductAttribute
from order.models import Discount
from payment.models import Payment
from users.models import User


def configure_admin_views(app):
    admin = Admin(app, name='Store', template_mode='bootstrap3')
    admin.add_view(ModelView(User))
    admin.add_view(ModelView(Product))
    admin.add_view(ModelView(Category))
    admin.add_view(ModelView(ProductAttribute))
    admin.add_view(ModelView(Payment))
    admin.add_view(ModelView(Discount))
    admin.add_view(ModelView(Line))
    admin.add_view(ModelView(Basket, endpoint="basket_"))
