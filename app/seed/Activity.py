from app import db
from app.models import Activity, Interest_Group
from datetime	import datetime


activities = [
	{
		'title'			: 'Fun Run',
		'description'	: 'Run Run Run',
		'start_date'	: '2017-09-19',
		'end_date'		: '2017-09-20',
		'address'		: 'Luneta Park',
		'group_id'		: Interest_Group.query.filter(Interest_Group.name=='Sports').first().id,
		'image'			: '70a256f3628947508af68343821d78b6.jpg'
	},
	{
		'title'			: 'Tech Summit',
		'description'	: 'Catch up with all the new trends with the technology',
		'start_date'	: '2017-09-19',
		'end_date'		: '2017-09-19',
		'address'		: 'Marco Polo',
		'group_id'		: Interest_Group.query.filter(Interest_Group.name=='Technology').first().id,
		'image'			: '8fc972debdde43568ab712730eb9f963.jpg'
	},
	{
		'title'			: 'Art Exhibit',
		'description'	: 'UnionBank Artists Exhibit',
		'start_date'	: '2017-09-21',
		'end_date'		: '2017-09-21',
		'address'		: '47th Floor, UnionBank Plaza',
		'group_id'		: Interest_Group.query.filter(Interest_Group.name=='Arts').first().id,
		'image'			: '56946b7fb0f64255af220a34664fd5a7.png'
	},
	{
		'title'			: 'Zumba Zumba',
		'description'	: 'UnionBank Zumba sa Umaga',
		'start_date'	: '2017-09-21',
		'end_date'		: '2017-09-21',
		'address'		: '48th Floor, UnionBank Plaza',
		'group_id'		: Interest_Group.query.filter(Interest_Group.name=='Zumba').first().id,
		'image'			: 'b31da3d4eaf54ed8a71a686f04c71ed0.jpg'
	},
	{
		'title'			: 'Mass',
		'description'	: 'Misa para sa Masa',
		'start_date'	: '2017-09-14',
		'end_date'		: '2017-09-14',
		'address'		: 'Ground Floor, UnionBank Plaza',
		'group_id'		: Interest_Group.query.filter(Interest_Group.name=='Family').first().id,
		'image'			: '402e8ec51b344f94b8c21f555f973004.png'
	},
	{
		'title'			: 'Liga',
		'description'	: '',
		'start_date'	: '2017-09-14',
		'end_date'		: '2017-09-15',
		'address'		: 'Valle Verde I',
		'group_id'		: Interest_Group.query.filter(Interest_Group.name=='Basketball').first().id,
		'image'			: 'liga.jpg'
	},
	{
		'title'			: 'Weekend Games',
		'description'	: '',
		'start_date'	: '2017-09-16',
		'end_date'		: '2017-09-16',
		'address'		: 'Valle Verde I',
		'group_id'		: Interest_Group.query.filter(Interest_Group.name=='Basketball').first().id,
		'image'			: 'juan.jpg'
	},
	{
		'title'			: 'Mobile Legends Tournament',
		'description'	: 'MoBa',
		'start_date'	: '2017-09-16',
		'end_date'		: '2017-09-16',
		'address'		: 'Valle Verde I',
		'group_id'		: Interest_Group.query.filter(Interest_Group.name=='Gamers').first().id,
		'image'			: 'mobile-legends-hack.png'
	},
	{
		'title'			: 'Sunday Trekking',
		'description'	: 'MoBa',
		'start_date'	: '2017-09-09',
		'end_date'		: '2017-09-09',
		'address'		: 'Mt. Mayon',
		'group_id'		: Interest_Group.query.filter(Interest_Group.name=='Hikers').first().id,
		'image'			: 'trek.jpg'
	},
	{
		'title'			: 'Free Checkup',
		'description'	: 'Medical mission for employees',
		'start_date'	: '2017-09-11',
		'end_date'		: '2017-09-11',
		'address'		: '48th Floor, Unionbank Plaza',
		'group_id'		: Interest_Group.query.filter(Interest_Group.name=='Medical').first().id,
		'image'			: 'medical.jpg'
	},
	{
		'title'			: 'UHAC AND PLAY: Employees Edition',
		'description'	: 'Hackathon for employees',
		'start_date'	: '2017-09-15',
		'end_date'		: '2017-09-17',
		'address'		: '48th Floor, Unionbank Plaza',
		'group_id'		: Interest_Group.query.filter(Interest_Group.name=='Technology').first().id,
		'image'			: 'hackathon.jpg'
	},
	{
		'title'			: 'Trending items',
		'description'	: 'Worthy shopping items',
		'start_date'	: '2017-09-18',
		'end_date'		: '2017-09-18',
		'address'		: '48th Floor, Unionbank Plaza',
		'group_id'		: Interest_Group.query.filter(Interest_Group.name=='Shopping').first().id,
		'image'			: 'best-shopping-in-Bucharest.jpg'
	}
]

for a in activities:
# for i in range(0, 15):
	activity = Activity.from_json(a)
	db.session.add(activity)
db.session.commit()