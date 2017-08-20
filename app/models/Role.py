from app import db
from app.models import Permission
from sqlalchemy_utils import UUIDType
import uuid

class Role(db.Model):
	__tablename__ = 'roles'
	id 			= db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
	name		= db.Column(db.String(64), unique=True)
	default 	= db.Column(db.Boolean, default=False, index=True)
	permissions = db.Column(db.Integer)
	users 		= db.relationship('User', backref='role', lazy='dynamic')