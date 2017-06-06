from flask import Flask
from flask_bootstrap import Bootstrap

from admin.views import configure_admin_views
from basket.processors import basket_processor
from basket.views import basket
from catalogue.views import catalogue
from database import db
from extensions import login_manager
from users.models import User, AnonymousUser
from users.views import users
from order.views import orders


def configure_blueprints(app):
    app.register_blueprint(users, url_prefix='/auth')
    app.register_blueprint(basket, url_prefix='/basket')
    app.register_blueprint(catalogue, url_prefix='/')
    app.register_blueprint(orders, url_prefix='/orders')


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    db.init_app(app)
    Bootstrap(app)
    configure_blueprints(app)
    configure_admin_views(app)

    app.secret_key = 'super secret key'

    return app


app = create_app()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    user_instance = User.query.filter_by(id=user_id).first()
    if user_instance:
        return user_instance
    else:
        return None


login_manager.anonymous_user = AnonymousUser
app.context_processor(basket_processor)

if __name__ == '__main__':
    app.run()
