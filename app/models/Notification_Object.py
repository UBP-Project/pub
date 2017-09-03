from flask import url_for
from app import db
from app.models import User, Follow
from sqlalchemy_utils import UUIDType
from datetime import datetime
import uuid

class Notification_Object(db.Model):
    __tablename__   = 'notification_object'
    id              = db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    entity_type_id  = db.Column(UUIDType(binary=False))
    entity_id       = db.Column(UUIDType(binary=False))
    created_on      = db.Column(db.DateTime)
    status          = db.Column(db.Boolean)

    def __init__(self, entity_type_id, entity_id):
        self.entity_type_id    = entity_type_id
        self.entity_id = entity_id
        self.created_on = datetime.utcnow()
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
