from app import db
from app.models import Notification, Notification_EntityType, Notification_Object, Notification_Change
from threading import Thread
from functools import wraps

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
			self.notif_object.set_active()
		else:
			self.notif_object = Notification_Object(entity_type.id, entity_id)

		db.session.add(self.notif_object)
		db.session.commit()

	def notif_object(entity, action, entity_id):
		#get the id of entity type
		entity_type = Notification_EntityType.query\
			.filter(Notification_EntityType.entity == entity, Notification_EntityType.action == action)\
			.first()

		return Notification_Object.query\
			.filter(Notification_Object.entity_type_id == entity_type.id, Notification_Object.entity_id == entity_id)\
			.first()

	def run_async(f):
		def async_func(*args, **kwargs):
			func = Thread(target=f, args=args, kwargs=kwargs)
			func.start()
			return func
		return async_func

	def add_actor(self, user_id):

		#check if the actor already had previous interaction
		change = Notification_Change.query.filter(Notification_Change.notification_object_id == self.notif_object.id, Notification_Change.actor_id == user_id).first()
		
		if change is None:
			# print("Notification Actor: " + str(user_id))
			actor = Notification_Change(self.notif_object.id, user_id)
			db.session.add(actor)
		# else:
		# 	print("Previously acted: " + str(user_id));

		db.session.commit()

	def add_notifiers(self, users):
		
		for user in users:
			
			#check if user was previously notified
			notification = Notification.query.filter(Notification.notification_object_id == self.notif_object.id, Notification.notifier_id == user.get_id()).first()

			if notification is None:
				# print("Notifying: "+ str(user.id))
				notifier = Notification(notification_object_id = self.notif_object.id, notifier_id = user.get_id())
				db.session.add(notifier)
			# else:
			# 	print("Previously notified: " + str(user.id));

		db.session.commit()