from app import db
from app.models import Notification_EntityType


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
		'action'	: 'followed_you'
	},
]

for e in entity_types:
	entity_type = Notification_EntityType.from_json(e)
	db.session.add(entity_type)
db.session.commit()