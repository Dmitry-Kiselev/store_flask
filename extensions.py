from celery import Celery
from flask_login import LoginManager

# Celery
celery = Celery("store_flask")

# Login
login_manager = LoginManager()
