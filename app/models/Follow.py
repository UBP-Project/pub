from app import db
from datetime import datetime

class Follow(db.Model):
    __tablename__   = 'follow'
    follower_id     = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    following_id    = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    timestamp       = db.Column(db.DateTime, default=datetime.utcnow())
    status          = db.Column(db.Integer) #0 pending #1 accepted

    def __init__(self, follower_id, following_id):
        self.follower_id    = follower_id
        self.following_id   = following_id
        self.datetime       = datetime.utcnow()
        self.status         = 0