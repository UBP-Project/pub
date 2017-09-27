from app import db
from app.models import Entity


entity_types = [
	{
		'entity'	: 'activity',
		'action'	: 'happening'
	},
	{
		'entity'	: 'activity',
		'action'	: 'joined'
	},
	{
		'entity'	: 'activity',
		'action'	: 'interested'
	},
	{
		'entity'	: 'activity',
		'action'	: 'attended'
	},
	{
		'entity'	: 'interest_group',
		'action'	: 'created_activity'
	},
	{
		'entity'	: 'interest_group',
		'action'	: 'updated_activity'
	},
	{
		'entity'	: 'interest_group',
		'action'	: 'deleted_activity'
	},
	{
		'entity'	: 'interest_group',
		'action'	: 'accepted_join_request'
	},
	{
		'entity'	: 'interest_group',
		'action'	: 'has_new_leader'
	},
	{
		'entity'	: 'user',
		'action'	: 'followed'
	},
]

for e in entity_types:
	entity_type = Entity.from_json(e)
	db.session.add(entity_type)
db.session.commit()