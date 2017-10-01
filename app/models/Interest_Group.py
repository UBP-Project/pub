from app import db
from datetime import datetime
from sqlalchemy_utils import UUIDType
import uuid
from app.models import User, Membership, Entity, Points_Type
import os
from werkzeug.utils import secure_filename


class Interest_Group(db.Model):
    __tablename__ = 'interest_group'
    id = db.Column(UUIDType(binary=False),
                   default=uuid.uuid4, primary_key=True)
    # change  to true on production
    name = db.Column(db.String(200), unique=False)
    about = db.Column(db.Text(4294967295))
    cover_photo = db.Column(db.String(100))
    group_icon = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, name, about, cover_photo="", group_icon=""):
        self.name = name
        self.about = about
        self.cover_photo = cover_photo
        self.group_icon = group_icon

    def __repr__(self):
        return '<Group %r>' % self.name

    def to_json(self):
        json_post = {
            'id': self.id,
            'name': self.name,
            'about': self.about,
            'cover_photo': self.cover_photo,
            'group_icon': self.group_icon
        }
        return json_post

    def set_points(self, action, value):
        entity_type = Entity.query.filter(
            Entity.entity == 'interest_group', Entity.action == action).first()
        points_type = Points_Type(
            entity_type.id, entity_id=self.id, value=value)
        db.session.add(points_type)
        db.session.commit()

    def edit_points(self, action, value):
        points_type = Points_Type.query\
            .join(Entity, Entity.id == Points_Type.entity_type_id)\
            .filter(Points_Type.entity_id == self.id,
                    Entity.entity == 'interest_group',
                    Entity.action == action).first()
        points_type.value = value
        db.session.commit()

    def get_points(self, action):
        points_type = Points_Type.query\
            .join(Entity, Entity.id == Points_Type.entity_type_id)\
            .filter(Points_Type.entity_id == self.id,
                    Entity.entity == 'interest_group',
                    Entity.action == action).first()
        return points_type.value

    def set_leader(self, user_id):
        membership = Membership.Membership.query.filter(
            Membership.Membership.group_id == self.id,
            Membership.Membership.user_id == user_id).first()
        membership.level = 1
        db.session.commit()

    def set_leaders(self, leader_ids):
        for leader_id in leader_ids:
            membership = Membership.Membership(
                group_id=self.id,
                user_id=leader_id,
                status=1,
                level=1)
            db.session.add(membership)
        db.session.commit()

    def get_leaders(self):
        leaders = User.User.query\
            .join(Membership.Membership, User.User.id == Membership.Membership.user_id) \
            .filter(Membership.Membership.group_id == self.id,
                    Membership.Membership.status != 0, Membership.Membership.level == 1).all()
        return leaders

    def remove_leader(self, user_id):
        membership = Membership.Membership.query.filter(
            Membership.Membership.group_id == self.id,
            Membership.Membership.user_id == user_id).first()
        membership.level = 0
        db.session.commit()

    def get_members(self):
        members = User.User.query \
            .join(Membership.Membership, User.User.id == Membership.Membership.user_id) \
            .filter(Membership.Membership.group_id == self.id,
                    Membership.Membership.status != 0, Membership.Membership.level == 0).all()
        return members

    def get_requests(self):
        requests = User.User.query.join(Membership.Membership, User.User.id == Membership.Membership.user_id) \
            .filter(Membership.Membership.group_id == self.id, Membership.Membership.status == 0,
                    Membership.Membership.level == 0).all()
        return requests

    def set_icon(self, icon):
        icon_filename = secure_filename(icon.filename)
        extension = icon_filename.rsplit('.', 1)[1].lower()
        icon_hashed_filename = str(uuid.uuid4().hex) + '.' + extension
        file_path = os.path.join('app/static/uploads/group_icons',
                                 icon_hashed_filename)
        icon.save(file_path)
        self.group_icon = icon_hashed_filename
        db.session.commit()

    def set_cover(self, cover):
        cover_filename = secure_filename(cover.filename)
        extension = cover_filename.rsplit('.', 1)[1].lower()
        cover_hashed_filename = str(uuid.uuid4().hex) + '.' + extension
        file_path = os.path.join('app/static/uploads/covers',
                                 cover_hashed_filename)
        cover.save(file_path)
        self.cover_photo = cover_hashed_filename
        db.session.commit()

    @staticmethod
    def from_json(json_interest_group):
        name = json_interest_group.get('name')
        about = json_interest_group.get('about')
        cover_photo = json_interest_group.get('cover_photo')
        group_icon = json_interest_group.get('group_icon')
        return Interest_Group(name=name, about=about,
                              cover_photo=cover_photo, group_icon=group_icon)
