from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from database import db
from search.commands.index import UpdateIndex
from store_flask import app

manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
manager.add_command('update_index', UpdateIndex)

if __name__ == "__main__":
    manager.run()
