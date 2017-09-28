from flask import url_for
from app import db
from sqlalchemy_utils import UUIDType
from datetime import datetime
from flask_login import login_required
import uuid

class Entity(db.Model):
    __tablename__   = 'entity'
    id              = db.Column(db.Integer, primary_key=True)
    entity          = db.Column(db.String(50))
    action          = db.Column(db.String(50))

    def __init__(self, entity, action):
        self.entity = entity
        self.action = action

    def get_entity(name, action):
        return Entity.query\
            .filter(entity == name)\
            .first()
        
    def __repr__(self):
        return '<Entity: %r>' % self.id

    def from_json(json_entity):
        entity    = json_entity.get('entity')
        action    = json_entity.get('action')
        return Entity(entity, action)