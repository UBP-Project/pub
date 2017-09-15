import uuid
from app import db
from sqlalchemy_utils import UUIDType
from datetime import datetime

class Points(db.Model):
	__tablename__ = 'points'
	id 			= db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
	user_id		= db.Column(UUIDType(binary=False), db.ForeignKey('user.id'))
	event		= db.Column(db.Text(4294967295)) #description for this point
	value		= db.Column(db.Integer, nullable=False)
	timestamp	= db.Column(db.DateTime, default=datetime.utcnow())

	def __init__(self, user_id, value, event = '', ):
		self.user_id = user_id
		self.event = event
		self.value = value

	def __repr__(self):
		return '<Points %r - %r>' % self.user_id, self.value

	def to_json(self):
		json = {
			'id'		: self.id,
			'user_id'	: self.user_id,
			'value'		: self.value,
			'event'		: self.event
		}

		return json

	@staticmethod
	def from_json(json):
		user_id		= json.get('user_id')
		value 		= json.get('value')
		event		= json.get('event')

		return Points(user_id,  value, event)