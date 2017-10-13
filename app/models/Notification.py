from flask import url_for
from app import db
from app.models import User, Follow
from sqlalchemy_utils import UUIDType
from sqlalchemy import func
from datetime import datetime
from flask_login import login_required
import uuid

class Notification_Object(db.Model):
    __tablename__   = 'notification_object'
    id              = db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    entity_type_id  = db.Column(db.Integer, db.ForeignKey('entity.id'))
    entity_id       = db.Column(UUIDType(binary=False))
    timestamp       = db.Column(db.DateTime, server_default=func.now())
    updated         = db.Column(db.DateTime, onupdate=func.now())
    status          = db.Column(db.Boolean)

    def __init__(self, entity_type_id, entity_id):
        self.entity_type_id    = entity_type_id
        self.entity_id = entity_id
        self.status = True

    def set_inactive(self):
        self.status = False
        db.session.commit()

    def set_active(self):
        self.status = True
        db.session.commit()

    def get_notif_object(id):
        return Notification_Object.query.get(id)
        
    def __repr__(self):
        return '<Notification_Object %r>' % self.id

class Notification(db.Model):
    __tablename__           = 'notification'
    id                      = db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    notification_object_id  = db.Column(UUIDType(binary=False), db.ForeignKey('notification_object.id'))
    actor_id                = db.Column(UUIDType(binary=False), db.ForeignKey('user.id'))
    timestamp               = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, notification_object_id, actor_id):
        self.notification_object_id    = notification_object_id
        self.actor_id = actor_id
        
    def __repr__(self):
        return '<Notification %r>' % self.id

    def to_json(self):
        return {
            'id' : self.id,
            'notification_object_id' : self.notification_object_id,
            'actor_id' : self.actor_id,
            'timestamp' : self.timestamp 
        }