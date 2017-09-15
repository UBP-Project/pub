import uuid
from app import db
from sqlalchemy_utils import UUIDType

class Perks(db.Model):
	__tablename__ = 'perks'
	id 			= db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
	title 		= db.Column(db.Text(4294967295), nullable=False)
	image 		= db.Column(db.String(200))
	description = db.Column(db.Text(4294967295))

	def __init_(self, title, image = '', description = ''):
		self.title = title
		self.image = image
		self.description = description

	def __repr__(self):
		return '<Perks %r>' % self.title

	def to_json(self):
		json = {
			'id'			: self.id,
			'title'			: self.title,
			'description'	: self.description,
			'image'			: self.image
		}

		return json

	@staticmethod
	def from_json(json):
		title		= json.get('title')
		description = json.get('description')
		image		= json.get('image')

		return Perks(title, image, description)