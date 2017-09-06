from app import db
# from app.models.guid import GUID
from sqlalchemy_utils import UUIDType
from datetime import datetime

class Membership(db.Model):

    MEMBERSHIP_PENDING  = 0
    MEMBERSHIP_ACCEPTED = 1
    MEMBERSHIP_DECLINED = 2

    MEMBERSHIP_MEMBER = 0
    MEMBERSHIP_LEADER = 1

    __tablename__     = 'membership'
    user_id     = db.Column(UUIDType(binary=False), db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    group_id    = db.Column(UUIDType(binary=False), db.ForeignKey('interest_group.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    timestamp   = db.Column(db.DateTime, default=datetime.utcnow())
    status      = db.Column(db.Integer)
    level       = db.Column(db.Integer)

    def __init__(self, user_id, group_id, status = MEMBERSHIP_PENDING, level = MEMBERSHIP_MEMBER):
        self.user_id = user_id
        self.group_id = group_id
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