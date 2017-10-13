from app import db
from sqlalchemy_utils import UUIDType
from sqlalchemy import func
from datetime import datetime
import uuid

class Comment(db.Model):
    __tablename__ = 'comment'
    id            = db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    user_id       = db.Column(UUIDType(binary=False), db.ForeignKey('user.id', ondelete="CASCADE", onupdate="CASCADE"))
    activity_id   = db.Column(UUIDType(binary=False), db.ForeignKey('activity.id', ondelete="CASCADE", onupdate="CASCADE"))
    timestamp     = db.Column(db.DateTime, server_default=func.now())
    updated       = db.Column(db.DateTime, onupdate=func.now())
    text          = db.Column(db.Text(4294967295))

    def __init__(user_id, activity_id, text):
        self.user_id        = user_id
        self.activity_id    = activity_id
        self.timestamp      = datetime.utcnow()
        self.text           = text

    def __repr__(self):
        return '<Comment %r>' % self.text