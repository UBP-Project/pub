#!/usr/bin/env python
import os
from app import create_app, db
from app.models import Interest_Group, User, Role
from app.seed import seed
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
import simulate
import test

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

# customise server for development only
server = Server(host="0.0.0.0", port=5000)
manager.add_command("runserver", server)

def create_admin():
	print("Create an administrator")
	firstname = input("Firstname: ")
	lastname = input("Lastname: ")
	email = input("Email: ")
	password = input("Password: ")
	department = input("Department: ")
	position = input("Position: ")
	admin_role = Role.query.filter(Role.name == "Administrator").first()

	admin_json = {
		'firstname': firstname,
		'lastname': lastname,
		'email': email,
		'password': password,
		'department': department,
		'position': position
	}

	admin = User.from_json(admin_json)
	admin.role_id = admin_role.id
	admin.password = password
	db.session.add(admin)
	db.session.commit()

def make_shell_context():
    return dict(app=app, db=db, Interest_Group=Interest_Group,
        User=User, Role=Role,
        seed=seed,
        simulate=simulate,
        test=test,
        create_admin=create_admin)
    
manager.add_command("shell", Shell(make_context=make_shell_context))

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
