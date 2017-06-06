from celery import Celery
from flask_cache import Cache
from flask_login import LoginManager

# Celery
celery = Celery("store_flask")

# Login
login_manager = LoginManager()

# Cache
cache = Cache(config={'CACHE_TYPE': 'redis'})
