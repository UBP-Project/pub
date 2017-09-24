from flask import jsonify
from flask_login import current_user, login_required
from app.models import Points_Type
from app.api_1_0 import api
from app import db

points = [
	{
		'name'	:	'Joined Activity',
		'value'	:	1
	},
	{
		'name'	:	'Joined Group',
		'value'	:	1
	}

]

for point in points:
	db.session.add(Points_Type.from_json(point))

db.session.commit()