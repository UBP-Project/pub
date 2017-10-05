from flask import jsonify
from app.models import Perks
from app.api_1_0 import api
from app import db
from PIL import Image
import uuid
import os

perks = [
	{
		'title'			:	'Perks of a Unionbanker',
		'description'	:	'10% discount on Marco Polo',
		'image'			:	'f45fdbb54cd443b389b28c0a39995481.jpg'
	}
]

for perk in perks:
	image_filename        = perk.get('image')
	extension             = image_filename.rsplit('.', 1)[1].lower()
	image_hashed_filename = str(uuid.uuid4().hex) + '.' + extension
	file_path             = os.path.join('app/static/uploads/perks_images/', image_hashed_filename)

	sizes = [
		(375, 240), # modal cover photo
		(164, 200)  # card
	]

	image = Image.open(os.path.join('app/static/uploads/perks_images/', image_filename))
	
	#resize image
	for size in sizes:
		basewidth = size[0]
		wpercent = (basewidth/float(image.size[0]))
		hsize = int((float(image.size[1])*float(wpercent)))

		new_image = image.resize((basewidth,hsize), Image.ANTIALIAS)

		directory = 'app/static/uploads/perks_images/' + str(size[0]) + 'x'+ str(size[1]) + '/'

		if not os.path.isdir(directory):
		    os.makedirs(directory)

		new_image.save(os.path.join(directory, image_hashed_filename), quality=100)

	perk['image'] = image_hashed_filename
	perk = Perks.from_json(perk)
	db.session.add(perk)
db.session.commit()