from app import db
from sqlalchemy_utils import UUIDType
from sqlalchemy import func
import uuid

class Assignment(db.Model):
    __tablename__ = 'assignment'
    id              = db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    activity_id     = db.Column(UUIDType(binary=False), db.ForeignKey('activity.id', ondelete="CASCADE", onupdate="CASCADE"))
    assigned_to     = db.Column(UUIDType(binary=False), db.ForeignKey('user.id', ondelete="CASCADE", onupdate="CASCADE"))
    initiated_by    = db.Column(UUIDType(binary=False), db.ForeignKey('user.id', ondelete="CASCADE", onupdate="CASCADE"))
    timestamp		= db.Column(db.DateTime, server_default=func.now())
    updated 		= db.Column(db.DateTime, onupdate=func.now())

    def __init__(self, activity_id, assigned_to, initiated_by):
        self.activity_id    = activity_id
        self.assigned_to    = assigned_to
        self.initiated_by   = initiated_by