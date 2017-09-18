from app import db
from app.models import Activity, Interest_Group, User, Notification, Notification_EntityType, Notification_Object
from threading import Thread
from functools import wraps
from flask import jsonify
import uuid
import asyncio

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

	def add_actor(self, user_id):

		#check if the actor already had previous interaction
		change = Notification.query.filter(Notification.notification_object_id == self.notif_object.id, Notification.actor_id == user_id).first()
		
		if change is None:
			actor = Notification(self.notif_object.id, user_id)
			db.session.add(actor)
		db.session.commit()

	def notif_object(entity, action, entity_id):

		#get the id of entity type
		entity_type = Notification_EntityType.query\
			.filter(Notification_EntityType.entity == entity, Notification_EntityType.action == action)\
			.first()

		return Notification_Object.query\
			.filter(Notification_Object.entity_type_id == entity_type.id, Notification_Object.entity_id == entity_id)\
			.first()

	def get_entity(entity, notification_object_id):

		if entity == 'activity':
			return Activity.query.filter(Activity.id==notification_object_id).first().to_json()
		elif entity == 'interest_group':
			return Interest_Group.query.filter(Interest_Group.id==notification_object_id).first().to_json()
		elif entity == 'user':
			user = User.query.filter(User.id == notification_object_id).first()
			return {
				'id'		: user.id,
				'firstname' : user.firstname,
				'middlename': user.middlename,
				'lastname'	: user.lastname,
				'email'		: user.email,
				'image'		: user.image
			}

	