from app import db
from datetime import datetime

class Membership(db.Model):
    __tablename__     = 'membership'
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    group_id    = db.Column(db.Integer, db.ForeignKey('interest_group.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    date_joined = db.Column(db.Date)
    status      = db.Column(db.Integer) #0 'pending', #1'accepted', #3'declined'
    level       = db.Column(db.Integer) #0 'regular' or #1'leader' member

    def __init__(self, user_id, group_id, status = 0, level = 0):
        self.user_id = user_id
        self.group_id = group_id
        self.date_joined = datetime.utcnow()
        self.status = status
        self.level = level

    def to_json(self):
        json_post = {
            'user_id'    : self.user_id,
            'group_id'   : self.group_id,
            'date_joined': self.date_joined,
            'status'     : self.status,
            'level'      : self.level
        }
        return json_post