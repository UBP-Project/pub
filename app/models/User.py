from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from app.models import Role, Permission, Follow, Points, Interest_Group, Membership, User_Activity, Activity, Points_Type, Entity
from sqlalchemy import func
from sqlalchemy_utils import UUIDType
from flask_login import UserMixin
import uuid
import getpass
import os
from uuid import UUID
from datetime import datetime
from flask_login import current_user
from flask import abort
from PIL import Image
from werkzeug.utils import secure_filename

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id            = db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    firstname     = db.Column(db.String(64))
    middlename    = db.Column(db.String(64), nullable=True)
    lastname      = db.Column(db.String(64))
    email         = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    department    = db.Column(db.String(100))
    position      = db.Column(db.String(100))
    birthday      = db.Column(db.Date)
    role_id       = db.Column(UUIDType(binary=False), db.ForeignKey('roles.id'))
    cover_photo   = db.Column(db.String(200))
    image         = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, server_default=func.now())
    updated = db.Column(db.DateTime, onupdate=func.now())
    
    def __init__(self, firstname, middlename, lastname, email, department, position, birthday, role_id, image=None):
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.email = email
        self.department = department
        self.position = position
        self.birthday = birthday
        self.role_id = role_id
        self.image = image

    def __repr__(self):
        return '<User %r>' % self.email

    def is_following(self, user):
        return self.followed.filter(Follow.follower_id == user.get_id).count() > 0

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self                     
    
    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions
    
    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def is_manager(self):
        if self.is_administrator():
            return True
        manager = Role.query.filter(Role.name == 'Manager').first()
        return (self.role_id == manager.id)

    def set_photo(self, image):
        image_filename = secure_filename(image.filename)
        extension = image_filename.rsplit('.', 1)[1].lower()
        image_hashed_filename = str(uuid.uuid4().hex) + '.' + extension
        file_path = os.path.join(
            'app/static/uploads/profile_pictures', image_hashed_filename)
        
        image.save(file_path)

        sizes = [
            (40, 40),   # icon
            (200, 200), # profile page
        ]

        image = Image.open(file_path)

        # resize image
        for size in sizes:
            basewidth = size[0]
            wpercent = (basewidth/float(image.size[0]))
            hsize = int((float(image.size[1])*float(wpercent)))

            new_image = image.resize((basewidth,hsize), Image.ANTIALIAS)

            directory = 'app/static/uploads/profile_pictures/' + \
                str(size[0]) + 'x' + str(size[1]) + '/'

            if not os.path.isdir(directory):
                os.makedirs(directory)

            new_image.save(os.path.join(directory, image_hashed_filename), quality=100)
        self.image = image_hashed_filename
        db.session.commit()

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.id

    def get_followers(self):
        return self.query.join(Follow, Follow.follower_id == User.id)\
                .order_by(Follow.timestamp.desc())\
                .filter(Follow.following_id == self.id).all()

    def get_following(self):
        return self.query.join(Follow, Follow.following_id == User.id)\
                    .filter(Follow.follower_id == self.id).all()

    def earn_point(self, event, entity, entity_id, action):
        #check the current value of the points_type table
        point_type = Points_Type.query.join(Entity).filter(Points_Type.entity_id == entity_id, Entity.entity == entity, Entity.action == action).first()

        if point_type is not None:
            point = Points(self.id, event, value = point_type.value)
        else:
            print("Giving default point value")
            point = Points(self.id, event)
        db.session.add(point)
        db.session.commit()

    def remove_point(self, event):
        points = Points.query.filter(Points.user_id == self.id, Points.event == event).delete()
        db.session.commit()

    def total_points(self):        
        user_points = Points.query\
            .with_entities(
                func.sum(Points.value).label("points")
            )\
            .join(User)\
            .filter(User.id == self.id)\
            .first()

        if user_points.points is not None:
            return user_points.points
        else:
            return 0

    def can_modify_group(self, group_id, abort_on_false=False):
        if self.is_manager() or self.is_administrator():
            return True
        is_leader = True if Membership.Membership.query.filter(
            Membership.Membership.group_id == group_id,
            Membership.Membership.user_id == self.id,
            Membership.Membership.level == 1).first() is not None else False
        if is_leader is False and abort_on_false is True:
            abort(403)
        return is_leader

    def can_modify_activity(self, activity_id, abort_on_false=False):
        if self.is_manager() or self.is_administrator():
            return True
        is_leader = Membership.Membership.query.join(Activity.Activity,
            Activity.Activity.group_id == Membership.Membership.group_id)\
            .filter(Membership.Membership.user_id == self.id,
            (Membership.Membership.level == 1) | (Membership.Membership.level == 2),
            Activity.Activity.id == activity_id).first() is not None
        if is_leader == False and abort_on_false == True:
            abort(403)
        return is_leader

    def to_json(self):
        json_post = {
            'id'           : self.id,
            'firstname'    : self.firstname,
            'middlename'   : self.middlename,
            'lastname'     : self.lastname,
            'email'        : self.email,
            'password_hash': self.password_hash,
            'department'   : self.department,
            'position'     : self.position,
            'birthday'     : self.birthday,
            'role_id'      : self.role_id,
            'cover_photo'  : self.cover_photo,
            'image'        : self.image
        }
        return json_post

    @staticmethod
    def from_json(json_user):
        firstname       = json_user.get('firstname')
        middlename      = json_user.get('middlename')
        lastname        = json_user.get('lastname')
        email           = json_user.get('email')
        password        = json_user.get('password')
        department      = json_user.get('department')
        position        = json_user.get('position')
        birthday        = json_user.get('birthday')
        role_id         = json_user.get('role')

        user = User(
            firstname       = firstname,
            middlename      = middlename,
            lastname        = lastname,
            email           = email,
            department      = department,
            position        = position,
            birthday        = birthday,
            role_id         = role_id
        )

        user.password = password
        return user

    @staticmethod
    def get(user_id):
        return User.query.get(user_id)

@login_manager.user_loader
def load_user(user_id):
    if type(user_id) is str:
        print("Is STR")
        return None
    return User.query.get(user_id)