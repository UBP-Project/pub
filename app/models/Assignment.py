from app import db
# from app.models import GUID()
from sqlalchemy_utils import UUIDType
import uuid

class Assignment(db.Model):
    __tablename__ = 'assignment'
    id              = db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    activity_id     = db.Column(UUIDType(binary=False), db.ForeignKey('activity.id', ondelete="CASCADE", onupdate="CASCADE"))
    assigned_to     = db.Column(UUIDType(binary=False), db.ForeignKey('user.id', ondelete="CASCADE", onupdate="CASCADE"))
    initiated_by    = db.Column(UUIDType(binary=False), db.ForeignKey('user.id', ondelete="CASCADE", onupdate="CASCADE"))

    def __init__(self, activity_id, assigned_to, initiated_by):
        self.activity_id    = activity_id
        self.assigned_to    = assigned_to
        self.initiated_by   = initiated_by