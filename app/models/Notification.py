from app import db
# from app.models.guid import GUID
from sqlalchemy_utils import UUIDType
from datetime import datetime
import uuid

class Notification(db.Model):
    __tablename__ = 'notification'
    id          = db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    user_id     = db.Column(UUIDType(binary=False))
    content     = db.Column(db.String(100))
    timestamp   = db.Column(db.Date)
    is_read     = db.Column(db.Boolean)

    def __init__(user_id, content):
        self.user_id    = user_id
        self.content    = content
        self.timestamp  = datetime.utcnow()
        self.is_read    = False
