from flask import url_for
from app import db
from app.models import User, Follow
from sqlalchemy_utils import UUIDType
from datetime import datetime
import uuid

class Notification_EntityType(db.Model):
    __tablename__   = 'notification_entity_type'
    id              = db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    entity          = db.Column(db.String(50))
    action          = db.Column(db.String(50))

    def __init__(self, entity, action):
        self.entity = entity
        self.action = action
        
    def __repr__(self):
        return '<Notification_Object %r>' % self.id

    # def to_json(self):
    #     json = {
    #         'id'        : self.id,
    #         'name'      : self.name
    #     }

    #     return json

    def from_json(json_entity):
        entity    = json_entity.get('entity')
        action    = json_entity.get('action')
        return Notification_EntityType(entity, action)
