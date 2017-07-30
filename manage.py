#!/usr/bin/env python
import os
from app import create_app, db
from app.models import Interest_Group, User
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

# customise server for development only
server = Server(host="0.0.0.0", port=5000)
manager.add_command("runserver", server)

def make_shell_context():
    return dict(app=app, db=db,
            Interest_Group=Interest_Group,
            User=User)
    
manager.add_command("shell", Shell(make_context=make_shell_context))

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()