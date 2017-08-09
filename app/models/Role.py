from app import db
from . import Permission

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	default = db.Column(db.Boolean, default=False, index=True)
	permissions = db.Column(db.Integer)
	users = db.relationship('User', backref='role', lazy='dynamic')

	@staticmethod
	def insert_roles():
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
			'Administrator': (0xff, False)
		}
		for r in roles:
			role = Role.query.filter_by(name=r).first()
			if role is None:
			    role = Role(name=r)
			role.permissions = roles[r][0]
			role.default = roles[r][1]
			db.session.add(role)
		db.session.commit()