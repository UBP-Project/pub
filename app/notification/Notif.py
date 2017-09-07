from app import db
from app.models import Notification, Notification_EntityType, Notification_Object, Notification_Change

class Notif():

	def __init__(self, entity, action, entity_id):

		#get the id of entity type
		entity_type = Notification_EntityType.query\
			.filter(Notification_EntityType.entity == entity, Notification_EntityType.action == action)\
			.first()

		#check if this object is already created
		temp_object = Notification_Object.query\
			.filter(Notification_Object.entity_type_id == entity_type.id, Notification_Object.entity_id == entity_id)\
			.first()

		#object is not yet added
		if temp_object is not None:
			self.notif_object = temp_object
		else:
			self.notif_object = Notification_Object(entity_type.id, entity_id)

		db.session.add(self.notif_object)
		db.session.commit()


	def add_actor(self, user_id):
		actor = Notification_Change(self.notif_object.id, user_id)
		db.session.add(actor)
		db.session.commit()

	def add_notifier(self, user_id):
		notifier = Notification(notification_object_id = self.notif_object.id, notifier_id = user_id)
		db.session.add(notifier)
		db.session.commit()