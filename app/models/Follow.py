from app import db
from sqlalchemy_utils import UUIDType
from sqlalchemy import func
from datetime import datetime

class Follow(db.Model):
    __tablename__   = 'follow'
    follower_id     = db.Column(UUIDType(binary=False), db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    following_id    = db.Column(UUIDType(binary=False), db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    timestamp       = db.Column(db.DateTime, server_default=func.now())
    status          = db.Column(db.Integer) #0 pending #1 accepted'

    # followed = db.relationship('User',
    #     # secondary = Follow,
    #     primaryjoin = (Follow.follower_id == id),
    #     # secondaryjoin = (Follow.following_id == id),
    #     backref=db.backref('User', lazy='dynamic'),
    #     lazy='dynamic'
    # )

    def __init__(self, follower_id, following_id):
        self.follower_id    = follower_id
        self.following_id   = following_id
        self.datetime       = datetime.utcnow()
        self.status         = 1