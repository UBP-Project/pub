from app import db
from datetime import datetime# from app.models.guid import GUID
from sqlalchemy_utils import UUIDType
import uuid
from datetime import datetime
from app.models import User, Membership

class Interest_Group(db.Model):
    __tablename__ = 'interest_group'
    id            = db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    name          = db.Column(db.String(200), unique=False) #change  to true on production
    about         = db.Column(db.Text(4294967295))
    cover_photo   = db.Column(db.String(200))
    group_icon    = db.Column(db.String(100))
    timestamp     = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, name, about, cover_photo = "", group_icon = ""):
        self.name           = name
        self.about          = about
        self.cover_photo    = cover_photo
        self.group_icon     = group_icon

    def __repr__(self):
        return '<Group %r>' % self.name

    def to_json(self):
        json_post = {
            'id'         : self.id,
            'name'       : self.name,
            'about'      : self.about,
            'cover_photo': self.cover_photo,
            'group_icon' : self.group_icon
        }
        return json_post

    @staticmethod
    def from_json(json_interest_group):
        name        = json_interest_group.get('name')
        about       = json_interest_group.get('about')
        cover_photo = json_interest_group.get('cover_photo')
        group_icon  = json_interest_group.get('group_icon')
        return Interest_Group(name=name, about=about, cover_photo=cover_photo, group_icon=group_icon)

    def get_members(self):
        return User.query.join(Membership, Membership.user_id == User.id)\
            .filter(Membership.group_id == self.id, Membership.status == 1, Membership.level == 0).all()

    def get_leaders(self):
        return User.query.join(Membership, Membership.user_id == User.id)\
            .filter(Membership.group_id == self.id, Membership.status == 1, Membership.level == 1).all()

    def get_managers(self):
        return User.query.join(Membership, Membership.user_id == User.id)\
            .filter(Membership.group_id == self.id, Membership.status == 1, Membership.level == 2).all()

    def set_leader(self, user_id):
        membership = Membership.query.filter(Membership.group_id == self.id, Membership.user_id == user_id).first()
        membership.level = 1
        db.session.commit()

    def remove_leader(self, user_id):
        membership = Membership.query.filter(Membership.group_id == self.id, Membership.user_id == user_id).first()
        membership.level = 0
        db.session.commit()

    def membership_requests(self):
        return User.query \
            .join(Membership, User.id==Membership.user_id) \
            .filter(Membership.group_id==id, Membership.status == 0, Membership.level == 0).all()