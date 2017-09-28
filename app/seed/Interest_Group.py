from app import db
from app.models import Interest_Group
import random
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
# for i in range(0, 20):
	group = Interest_Group.from_json(g)
	group.set_points('accepted_join_request', random.randint(10, 20))
	db.session.add(group)
db.session.commit()