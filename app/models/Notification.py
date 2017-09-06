from flask import url_for
from app import db
from app.models import User, Follow
from sqlalchemy_utils import UUIDType
from datetime import datetime
import uuid

class Notification_EntityType(db.Model):
    __tablename__   = 'notification_entity_type'
    id              = db.Column(db.Integer, primary_key=True)
    entity          = db.Column(db.String(50))
    action          = db.Column(db.String(50))

    def __init__(self, entity, action):
        self.entity = entity
        self.action = action

    def get_entity(name, action):
        return Notification_EntityType.query\
            .filter(entity == name)\
            .first()
        
    def __repr__(self):
        return '<Notification_Object %r>' % self.id

    def from_json(json_entity):
        entity    = json_entity.get('entity')
        action    = json_entity.get('action')
        return Notification_EntityType(entity, action)

class Notification_Object(db.Model):
    __tablename__   = 'notification_object'
    id              = db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    entity_type_id  = db.Column(db.Integer, db.ForeignKey('notification_entity_type.id'))
    entity_id       = db.Column(UUIDType(binary=False))
    timestamp       = db.Column(db.DateTime)
    status          = db.Column(db.Boolean)

    def __init__(self, entity_type_id, entity_id):
        self.entity_type_id    = entity_type_id
        self.entity_id = entity_id
        self.timestamp = datetime.utcnow()
        self.status = False
        
    def __repr__(self):
        return '<Notification_Object %r>' % self.id

class Notification_Change(db.Model):
    __tablename__           = 'notification_change'
    id                      = db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    notification_object_id  = db.Column(UUIDType(binary=False), db.ForeignKey('notification_object.id'))
    actor_id                = db.Column(UUIDType(binary=False), db.ForeignKey('user.id'))
    status                  = db.Column(db.Boolean)

    def __init__(self, notification_object_id, actor_id):
        self.notification_object_id    = notification_object_id
        self.actor_id = actor_id
        self.status = False
        
    def __repr__(self):
        return '<Notification_Object %r>' % self.id


class Notification(db.Model):
    __tablename__ = 'notification'
    id          = db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    notification_object_id = db.Column(UUIDType(binary=False), db.ForeignKey('notification_object.id'))
    notifier_id            = db.Column(UUIDType(binary=False), db.ForeignKey('user.id'))
    status                 = db.Column(db.Boolean)
    timestamp              = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, notification_object_id, notifier_id):
        self.notification_object_id = notification_object_id
        self.notifier_id = notifier_id
        self.status = False

    def __repr__(self):
        return '<Notification %r>' % self.id

