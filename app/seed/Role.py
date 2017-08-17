from app import db
from app.models import Role, Permission

roles = {
	'User': (Permission.FOLLOW |
	    Permission.COMMENT, True),
	'Manager': (Permission.FOLLOW |
	    Permission.COMMENT |
	    Permission.CREATE_ACTIVITY |
	    Permission.CREATE_GROUP |
	    Permission.MANAGE_USERS |
	    Permission.MANAGE_GROUP |
	    Permission.MANAGE_ACTIVITY , False),
	'Administrator': (0xff, False)}

for r in roles:
	role = Role.query.filter_by(name=r).first()
	if role is None:
	    role = Role(name=r)
	role.permissions = roles[r][0]
	role.default = roles[r][1]
	db.session.add(role)

db.session.commit()