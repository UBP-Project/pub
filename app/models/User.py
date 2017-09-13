from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from app.models import Role, Permission, Follow
from sqlalchemy_utils import UUIDType
from flask_login import UserMixin
import uuid
import getpass
from uuid import UUID
from datetime import datetime


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
    points        = db.Column(db.Integer, default=0)
    cover_photo   = db.Column(db.String(200))
    image         = db.Column(db.String(100))
    timestamp     = db.Column(db.DateTime, default=datetime.utcnow())
    
    # followed      = db.relationship('Follow', foreign_keys=[Follow.follower_id], backref=db.backref('follower', lazy='joined'), lazy='dynamic', passive_deletes=True, passive_updates=True)
    # follower      = db.relationship('Follow', foreign_keys=[Follow.following_id], backref=db.backref('followed', lazy='joined'), passive_deletes=True, passive_updates=True)

    # followed = db.relationship('User',
    #     secondary = Follow,
    #     primaryjoin = (Follow.follower_id == id),
    #     secondaryjoin = (Follow.follower_id == id),
    #     backref = db.backref('Follow', lazy='dynamic'),
    #     lazy='dynamic'
    #     )

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

    # def __init__(self, firstname, middlename, lastname, email, password_hash, department, position, birthday, role_id):
    #     self.firstname = firstname
    #     self.middlename = middlename
    #     self.lastname = lastname
    #     self.email = email
    #     self.password_hash = password_hash
    #     self.department = department
    #     self.position = position
    #     self.birthday = birthday
    #     self.role_id = role_id
                     
    
    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions
    
    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def __repr__(self):
        return '<User %r>' % self.email

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
        return User.query\
            .join(Follow, Follow.following_id==self.id)\
            .filter(id != self.id)\
            .all()

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
            'points'       : self.points,
            'cover_photo'  : self.points,
            'image'        : self.image
        }
        return json_post

    @staticmethod
    def from_json(json_user):
        firstname       = json_user.get('firstname')
        middlename      = json_user.get('middlename')
        lastname        = json_user.get('lastname')
        email           = json_user.get('email')
        password        = json_user.get('password_hash')
        department      = json_user.get('department')
        position        = json_user.get('position')
        birthday        = json_user.get('birthday')
        role_id         = json_user.get('role')

        return User(
            firstname       = firstname,
            middlename      = middlename,
            lastname        = lastname,
            email           = email,
            password_hash   = password,
            department      = department,
            position        = position,
            birthday        = birthday,
            role_id         = role_id
        )

    def get_user_by_id(id):
        return User.query.get(id)

@login_manager.user_loader
def load_user(user_id):
    if type(user_id) is str:
        print("Is STR")
        return None
    return User.query.get(user_id)