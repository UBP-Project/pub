from app import db
from app.models import Role, User
from werkzeug.security import generate_password_hash

admin = [
	{
		'firstname'		:	'UnionBank',
		'lastname'		:	'Admin',
		'email'			:	'admin@unionbank.com',
		'password_hash'	:	'admin',
		'department'	:	'Talent Acquisition',
		'position'		:	'Head'
	}]

admin_role = Role.query.filter(Role.name == "Administrator").first()

for a in admin:
	admin = User.from_json(a)
	admin.role_id = admin_role.id
	admin.password_hash = generate_password_hash(admin.password_hash)
	db.session.add(admin)
db.session.commit()

users = [
	{
		'firstname'		:	'Red',
		'middlename'	:	'Awa',
		'lastname'		:	'Periabras',
		'email'			:	'redperiabras@gmail.com',
		'password_hash'	:	'12345',
		'department'	:	'Business Analytics',
		'position'		:	'Project Hire',
		'birthday'		:	'1998-02-01'
	},
	{
		'firstname'		:	'Ariel',
		'middlename'	:	'Soneja',
		'lastname'		:	'Conde',
		'email'			:	'asconde1997@gmail.com',
		'password_hash'	:	'12345',
		'department'	:	'Business Analytics',
		'position'		:	'Project Hire',
		'birthday'		:	'1997-09-07'
	},
	{
		'firstname'		:	'Prince Julius',
		'middlename'	:	'Torres',
		'lastname'		:	'Hari',
		'email'			:	'princejulius230@gmail.com',
		'password_hash'	:	'12345',
		'department'	:	'Business Analytics',
		'position'		:	'Project Hire',
		'birthday'		:	'1997-07-23'
	},
	{
		'firstname'		:	'Test',
		'middlename'	:	'Test',
		'lastname'		:	'Test',
		'email'			:	'test@gmail.com',
		'password_hash'	:	'test',
		'department'	:	'Business Analytics',
		'position'		:	'Project Hire',
		'birthday'		:	'1997-09-07'
	}
] 

user_role = Role.query.filter(Role.name == "User").first()

for u in users:
	user = User.from_json(u)
	user.role_id = user_role.id
	user.password_hash = generate_password_hash(user.password_hash)
	db.session.add(user)
db.session.commit()
