from flask import Flask
from flask_bootstrap import Bootstrap

from admin.views import configure_admin_views
from basket.processors import basket_processor
from basket.views import basket
from catalogue.views import catalogue
from database import db
from extensions import login_manager, cache
from order.views import orders
from search.views import search
from users.models import User, AnonymousUser
from users.views import users


def configure_blueprints(app):
    app.register_blueprint(users, url_prefix='/auth')
    app.register_blueprint(basket, url_prefix='/basket')
    app.register_blueprint(catalogue, url_prefix='/')
    app.register_blueprint(orders, url_prefix='/orders')
    app.register_blueprint(search, url_prefix='/search')


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    db.init_app(app)
    login_manager.init_app(app)
    cache.init_app(app)
    Bootstrap(app)
    configure_blueprints(app)
    configure_admin_views(app)

    return app


app = create_app()


@login_manager.user_loader
def load_user(user_id):
    user_instance = User.objects.get(id=user_id)
    if user_instance:
        return user_instance
    else:
        return None


login_manager.anonymous_user = AnonymousUser
app.context_processor(basket_processor)

if __name__ == '__main__':
    app.run()
