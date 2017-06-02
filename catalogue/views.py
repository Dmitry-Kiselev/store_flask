from .models import Category, Product
from flask_generic_views import TemplateView, RedirectView
from flask import Blueprint


catalogue = Blueprint("catalogue", __name__)

index = TemplateView.as_view('index', template_name='catalogue/index.html')

catalogue.add_url_rule('/', view_func=index,  defaults={
    #'categories': Category.query.all(), 'products': Product.query.all()
})