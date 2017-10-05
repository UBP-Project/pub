import uuid
from app import db
from sqlalchemy_utils import UUIDType
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from PIL import Image

class Perks(db.Model):
	__tablename__ = 'perks'
	id 			= db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
	title 		= db.Column(db.Text(4294967295), nullable=False)
	image 		= db.Column(db.String(200))
	description = db.Column(db.Text(4294967295))
	timestamp   = db.Column(db.DateTime, default=datetime.utcnow())

	def __init__(self, title, description, image=""):
		self.title = title
		self.image = image
		self.description = description

	def __repr__(self):
		return '<Perks %r>' % self.title

	def to_json(self):
		json = {
			'id'         : self.id,
			'title'      : self.title,
			'description': self.description,
			'image'      : self.image,
			'timestamp'  : self.timestamp
		}

		return json

	def set_image(self, image):
		image_filename = secure_filename(image.filename)
		extension = image_filename.rsplit('.', 1)[1].lower()
		image_hashed_filename = str(uuid.uuid4().hex) + '.' + extension
		file_path = os.path.join(
		'app/static/uploads/perks_images', image_hashed_filename)

		image.save(file_path)

		sizes = [
			(375, 240), # modal cover photo
			(164, 200)  # card
		]

		image = Image.open(file_path)

		# resize image
		for size in sizes:
			basewidth = size[0]
			wpercent = (basewidth/float(image.size[0]))
			hsize = int((float(image.size[1])*float(wpercent)))

			new_image = image.resize((basewidth,hsize), Image.ANTIALIAS)

			directory = 'app/static/uploads/perks_images/' + \
			    str(size[0]) + 'x' + str(size[1]) + '/'

			if not os.path.isdir(directory):
			    os.makedirs(directory)

			new_image.save(os.path.join(directory, image_hashed_filename))
		self.image = image_hashed_filename
		db.session.commit()

	@staticmethod
	def from_json(json):
		title		= json.get('title')
		description = json.get('description')
		image		= json.get('image')

		return Perks(title, description, image)