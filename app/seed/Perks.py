from flask import jsonify
from app.models import Perks
from app.api_1_0 import api
from app import db

perks = [
	{
		'title'			:	'Perks of a Unionbanker',
		'description'	:	'10% discount on Marco Polo',
		'image'			:	'f45fdbb54cd443b389b28c0a39995481.jpg'
	}
]

for perk in perks:
	db.session.add(Perks.from_json(perk))

db.session.commit()