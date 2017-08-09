from app import db
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comment'
    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE", onupdate="CASCADE"))
    activity_id   = db.Column(db.Integer, db.ForeignKey('activity.id', ondelete="CASCADE", onupdate="CASCADE"))
    timestamp     = db.Column(db.Time, default=datetime.utcnow) #set default to system's current time
    text          = db.Column(db.String(300))

    def __init__(user_id, activity_id, text):
        self.user_id        = user_id
        self.activity_id    = activity_id
        self.timestamp      = datetime.utcnow()
        self.text           = text

    def __repr__(self):
        return '<Comment %r>' % self.text