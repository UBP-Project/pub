from app import db
# from app.models.guid import GUID
from sqlalchemy_utils import UUIDType
from datetime import datetime
import uuid

class Comment(db.Model):
    __tablename__ = 'comment'
    id            = db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    user_id       = db.Column(UUIDType(binary=False), db.ForeignKey('user.id', ondelete="CASCADE", onupdate="CASCADE"))
    activity_id   = db.Column(UUIDType(binary=False), db.ForeignKey('activity.id', ondelete="CASCADE", onupdate="CASCADE"))
    timestamp     = db.Column(db.Time, default=datetime.utcnow()) #set default to system's current time
    text          = db.Column(db.String(300))

    def __init__(user_id, activity_id, text):
        self.user_id        = user_id
        self.activity_id    = activity_id
        self.timestamp      = datetime.utcnow()
        self.text           = text

    def __repr__(self):
        return '<Comment %r>' % self.text