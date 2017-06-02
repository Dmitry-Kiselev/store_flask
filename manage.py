from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from database import db
from store_flask import app

manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
