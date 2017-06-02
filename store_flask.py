from flask import Flask
from flask_bootstrap import Bootstrap

from extensions import login_manager
from users.models import User, AnonymousUser
from users.views import users
from database import configure_db, db


def configure_blueprints(app):
    app.register_blueprint(users, url_prefix='/auth')


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    configure_blueprints(app)

    app.secret_key = 'super secret key'

    return app


app = create_app()
db.init_app(app)
login_manager.init_app(app)
configure_db(app)


@login_manager.user_loader
def load_user(user_id):
    user_instance = User.query.filter_by(id=user_id).first()
    if user_instance:
        return user_instance
    else:
        return None

login_manager.anonymous_user = AnonymousUser


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
