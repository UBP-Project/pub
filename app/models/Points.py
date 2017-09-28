import uuid
from app import db
from sqlalchemy_utils import UUIDType
from datetime import datetime

class Points_Type(db.Model):
	__tablename__ = 'points_type'
	id 				= db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
	entity_type_id  = db.Column(db.Integer, db.ForeignKey('entity.id'))
	entity_id       = db.Column(UUIDType(binary=False))
	value			= db.Column(db.Integer())

 	# timestamp       = db.Column(db.DateTime)
	# name = db.Column(db.String(50))
	# value = db.Column(db.Integer)

	def __init__(self, entity_type_id, entity_id, value):  
		self.entity_type_id    = entity_type_id
		self.entity_id = entity_id
		self.value = value

	def __repr__(self):
		return '<Points_Type %r>' % self.id

	# @staticmethod
	# def from_json(json):
	# 	return Points_Type(json.get('name'), json.get('value'))

	# @staticmethod
	# def get_type_id(name):
	# 	return Points_Type.query.filter(Points_Type.name == name).first().id
	
class Points(db.Model):
	__tablename__ = 'points'
	id 			= db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
	user_id		= db.Column(UUIDType(binary=False), db.ForeignKey('user.id'))
	event		= db.Column(db.Text(4294967295)) #description for this point
	value		= db.Column(db.Integer())
	timestamp	= db.Column(db.DateTime, default=datetime.utcnow())

	def __init__(self, user_id, event, value = 1):
		self.user_id = user_id
		self.event = event
		self.value = value

	def __repr__(self):
		return '<Points %r - %r>' % self.user_id, self.type

	def to_json(self):
		json = {
			'id'		: self.id,
			'user_id'	: self.user_id,
			'event'		: self.event,
			'value'		: self.value
		}

		return json

	@staticmethod
	def from_json(json):
		user_id		= json.get('user_id')
		type		= json.get('type')

		return Points(user_id, event, value)