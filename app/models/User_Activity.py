from app import db
# from app.models.guid import GUID
from sqlalchemy_utils import UUIDType
import uuid

class User_Activity(db.Model):
    __tablename__ = 'user_activity'
    id          = db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    user_id     = db.Column(UUIDType(binary=False), db.ForeignKey('user.id', ondelete="CASCADE", onupdate="CASCADE"))
    activity_id = db.Column(UUIDType(binary=False), db.ForeignKey('activity.id', ondelete="CASCADE", onupdate="CASCADE"))
    status      = db.Column(db.Integer) #0 interested #1 going
    
    def __init__(self, user_id, activity_id, status = 0):
        self.user_id = user_id
        self.activity_id = activity_id
        self.status = status