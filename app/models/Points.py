import uuid
from app import db
from sqlalchemy_utils import UUIDType
from datetime import datetime

class Points_Type(db.Model):
	__tablename__ = 'points_type'
	id = db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
	name = db.Column(db.String(50))
	value = db.Column(db.Integer)

	def __init__(self, name, value):
		self.name = name
		self.value = value

	def __repr__(self):
		return '<Points_Type %r - %r>' % self.name, self.value

	@staticmethod
	def from_json(json):
		return Points_Type(json.get('name'), json.get('value'))

	@staticmethod
	def get_type_id(name):
		return Points_Type.query.filter(Points_Type.name == name).first().id

class Points(db.Model):
	__tablename__ = 'points'
	id 			= db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
	user_id		= db.Column(UUIDType(binary=False), db.ForeignKey('user.id'))
	event		= db.Column(db.Text(4294967295)) #description for this point
	type		= db.Column(UUIDType(binary=False), db.ForeignKey('points_type.id'))
	timestamp	= db.Column(db.DateTime, default=datetime.utcnow())

	def __init__(self, user_id, event, type):
		self.user_id = user_id
		self.event = event
		self.type = type

	def __repr__(self):
		return '<Points %r - %r>' % self.user_id, self.type

	def to_json(self):
		json = {
			'id'		: self.id,
			'user_id'	: self.user_id,
			'type'		: self.type
		}

		return json

	@staticmethod
	def from_json(json):
		user_id		= json.get('user_id')
		type		= json.get('type')

		return Points(user_id, value, event)