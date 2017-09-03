from flask import url_for
from app import db
from app.models import User, Follow
from sqlalchemy_utils import UUIDType
from datetime import datetime
import uuid

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

    # def to_json(self):
    #     json = {
    #         'id'        : self.id,
    #         'name'      : self.name
    #     }

    #     return json

    # def from_json(json_notification):
    #     name    = json_notification.get('name')
    #     return Notification_Type(name)
