from app import db
from app.models import Interest_Group

groups = [
	{
		'name'			: 'Sports',
		'about'			: 'Everything you should get involved!',
		'cover_photo'	: 'c94f84619ce845f3b6398a30aa99c720.bmp',
		'group_icon'	: 'd167f8ec77194efc8319e3455da9920f.jpg'
	},
	{
		'name'			: 'Techies',
		'about'			: 'Technology Events',
		'cover_photo'	: 'c0b5cfd73486428ba70fddd88f045035.jpg',
		'group_icon'	: 'ee7c6819aa804255a2a3f1a9bd5732d3.jpg'
	},
	{
		'name'			: 'Umba',
		'about'			: 'Morning Zumba Events',
		'cover_photo'	: '00771563eb6748b284b713294905777e.jpg',
		'group_icon'	: '91c4cd4954e14555808e5649653c7666.jpg'
	},
	{
		'name'			: 'Arts',
		'about'			: 'Artsy People',
		'cover_photo'	: '5e7a66a709234aed9f690b80de8434e2.jpg',
		'group_icon'	: 'fbb59b05434d461c932f031029b66562.jpg'
	}
]

for g in groups:
	group = Interest_Group.from_json(g)
	db.session.add(group)
db.session.commit()