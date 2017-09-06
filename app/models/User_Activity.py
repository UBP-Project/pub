from app import db
from datetime import datetime
from sqlalchemy_utils import UUIDType
import uuid
from datetime import datetime

class User_Activity(db.Model):
    __tablename__ = 'user_activity'
    id            = db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    user_id       = db.Column(UUIDType(binary=False), db.ForeignKey('user.id', ondelete="CASCADE", onupdate="CASCADE"))
    activity_id   = db.Column(UUIDType(binary=False), db.ForeignKey('activity.id', ondelete="CASCADE", onupdate="CASCADE"))
    status        = db.Column(db.Integer) #0 interested #1 going
    attended      = db.Column(db.Boolean)
    timestamp     = db.Column(db.DateTime, default=datetime.utcnow())
    
    def __init__(self, user_id, activity_id, status = 0):
        self.user_id = user_id
        self.activity_id = activity_id
        self.status = status