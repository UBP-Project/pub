from app import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    content = db.Column(db.String(100))
    timestamp = db.Column(db.Date)
    is_read = db.Column(db.Boolean)

    def __init__(user_id, content):
        self.user_id    = user_id
        self.content    = content
        self.timestamp  = datetime.utcnow()
        self.is_read    = false
