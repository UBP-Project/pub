from app import db
from app.models import Interest_Group
import random
from PIL import Image
from werkzeug.utils import secure_filename
import os
import uuid
groups = [
	{
		'name'			: 'Sports',
		'about'			: 'Everything you should get involved!',
		'cover_photo'	: 'c94f84619ce845f3b6398a30aa99c720.bmp',
		'group_icon'	: 'd167f8ec77194efc8319e3455da9920f.jpg'
	},
	{
		'name'			: 'Technology',
		'about'			: 'Technology Enthusiast',
		'cover_photo'	: 'tech.jpg',
		'group_icon'	: 'tech.jpg'
	},
	{
		'name'			: 'Zumba',
		'about'			: 'Morning Zumba Events',
		'cover_photo'	: '00771563eb6748b284b713294905777e.jpg',
		'group_icon'	: '91c4cd4954e14555808e5649653c7666.jpg'
	},
	{
		'name'			: 'Arts',
		'about'			: 'Artsy People',
		'cover_photo'	: '5e7a66a709234aed9f690b80de8434e2.jpg',
		'group_icon'	: 'fbb59b05434d461c932f031029b66562.jpg'
	},
	{
		"name"			: "Basketball",
		"about"			: "Where basket is life! Puso!!!",
		"cover_photo"	: "bball.jpg",
		"group_icon"	: "bball.jpeg"
	},
	{
		'name'			: 'Badminton',
		'about'			: '',
		'cover_photo'	: 'badminton.jpg',
		'group_icon'	: 'badminton.jpg'
	},
	{
		'name'			: 'Volleyball',
		'about'			: '',
		'cover_photo'	: 'volley.jpg',
		'group_icon'	: 'volley.jpg'
	},
	{
		'name'			: 'Millennials',
		'about'			: 'Hello, we are millennials',
		'cover_photo'	: 'millenials.jpg',
		'group_icon'	: 'millenials.jpg'
	},
	{
		'name'			: 'Family',
		'about'			: 'Family Time',
		'cover_photo'	: 'family.jpg',
		'group_icon'	: 'family.jpg'
	},
	{
		'name'			: 'Gamers',
		'about'			: 'Republic of Gamers',
		'cover_photo'	: 'gamer.jpg',
		'group_icon'	: 'gamer.jpg'
	},
	{
		'name'			: 'Hikers',
		'about'			: 'Mountaineering Group',
		'cover_photo'	: 'hike.jpg',
		'group_icon'	: 'hike.jpg'
	},
	{
		'name'			: 'Medical',
		'about'			: 'Health and More',
		'cover_photo'	: 'medical.jpg',
		'group_icon'	: 'medical.jpg'
	}, 
	{
		'name'			: 'Shopping',
		'about'			: 'Shoppaholics',
		'cover_photo'	: 'shop.jpg',
		'group_icon'	: 'shop.jpg'
	}
]

for g in groups:
	icon_filename = g.get('group_icon')
	extension = icon_filename.rsplit('.', 1)[1].lower()
	icon_hashed_filename = str(uuid.uuid4().hex) + '.' + extension
	file_path = os.path.join('app/static/uploads/group_icons',icon_hashed_filename)

	icon_sizes = [
		(130, 130), #card icon
		(200, 200), #modal icon
	]

	icon = Image.open(os.path.join('app/static/uploads/group_icons/', g.get('group_icon')))
	icon.save(file_path)

	#resize icon
	for size in icon_sizes:
		new_image = icon.resize(size, Image.ANTIALIAS)

		directory = 'app/static/uploads/group_icons/' + str(size[0]) + 'x'+ str(size[1]) + '/'

		if not os.path.isdir(directory):
			os.makedirs(directory)

		new_image.save(os.path.join(directory, icon_hashed_filename), quality=100)

	g['group_icon'] = icon_hashed_filename

	cover_filename = g.get('cover_photo')
	extension = cover_filename.rsplit('.', 1)[1].lower()
	cover_hashed_filename = str(uuid.uuid4().hex) + '.' + extension
	file_path = os.path.join('app/static/uploads/covers',cover_hashed_filename)

	cover_sizes = [
		(200, 170), #card cover
		(600, 250)  #modal cover
	]

	cover = Image.open(os.path.join('app/static/uploads/covers/', g.get('cover_photo')))
	cover.save(file_path)

	#resize icon
	for size in cover_sizes:
		new_image = cover.resize(size, Image.ANTIALIAS)

		directory = 'app/static/uploads/covers/' + str(size[0]) + 'x'+ str(size[1]) + '/'

		if not os.path.isdir(directory):
			os.makedirs(directory)

		new_image.save(os.path.join(directory, cover_hashed_filename), quality=100)

	g['cover_photo'] = cover_hashed_filename

	group = Interest_Group.from_json(g)
	db.session.add(group)
db.session.commit()

groups = Interest_Group.query.all()

for group in groups:
	group.set_points('accepted_join_request', random.randint(10, 20))
db.session.commit()