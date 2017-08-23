from app import db
from app.models import Activity, Interest_Group
from datetime	import datetime

sport_group = Interest_Group.query.filter(Interest_Group.name=='Sports').first()
tech_group	= Interest_Group.query.filter(Interest_Group.name=='Techies').first()
zumba_group = Interest_Group.query.filter(Interest_Group.name=='Umba').first()
arts_group	= Interest_Group.query.filter(Interest_Group.name=='Arts').first()

activities = [
	{
		'title'			: 'Fun Run',
		'description'	: 'Run Run Run',
		'start_date'	: '2017-08-19',
		'end_date'		: '2017-08-20',
		'address'		: 'Luneta Park',
		'group_id'		: sport_group.id,
		'image'			: '70a256f3628947508af68343821d78b6.jpg'
	},
	{
		'title'			: 'Tech Summit',
		'description'	: 'Catch up with all the new trends with the technology',
		'start_date'	: '2017-08-19',
		'end_date'		: '2017-08-19',
		'address'		: 'Marco Polo',
		'group_id'		: tech_group.id,
		'image'			: '8fc972debdde43568ab712730eb9f963.jpg'
	},
	{
		'title'			: 'Art Exhibit',
		'description'	: 'UnionBank Artists Exhibit',
		'start_date'	: '2017-08-21',
		'end_date'		: '2017-08-21',
		'address'		: '47th Floor, UnionBank Plaza',
		'group_id'		: arts_group.id,
		'image'			: '56946b7fb0f64255af220a34664fd5a7.png'
	},
	{
		'title'			: 'Zumba Zumba',
		'description'	: 'UnionBank Zumba sa Umaga',
		'start_date'	: '2017-08-21',
		'end_date'		: '2017-08-21',
		'address'		: '48th Floor, UnionBank Plaza',
		'group_id'		: zumba_group.id,
		'image'			: 'b31da3d4eaf54ed8a71a686f04c71ed0.jpg'
	},
	{
		'title'			: 'Daily Mass',
		'description'	: 'Misa para sa Masa',
		'start_date'	: '2017-08-14',
		'end_date'		: '2017-08-14',
		'address'		: 'Ground Floor, UnionBank Plaza',
		'image'			: '402e8ec51b344f94b8c21f555f973004.png'
	}
]

for a in activities:
	activity = Activity.from_json(a)
	db.session.add(activity)
db.session.commit()