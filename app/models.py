from datetime import datetime
from app import db
from . import login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Follow(db.Model):
    __tablename__   = 'follow'
    follower_id     = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    following_id    = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    timestamp       = db.Column(db.DateTime, default=datetime.utcnow())
    status          = db.Column(db.Integer) #0 pending #1 accepted

    def __init__(self, follower_id, following_id):
        self.follower_id    = follower_id
        self.following_id   = following_if
        self.datetime       = datetime.utcnow()
        self.status         = 0

class Assignment(db.Model):
    __tablename__ = 'assignment'
    id              = db.Column(db.Integer, primary_key=True)
    activity_id     = db.Column(db.Integer, db.ForeignKey('activity.id', ondelete="CASCADE", onupdate="CASCADE"))
    assigned_to     = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE", onupdate="CASCADE"))
    initiated_by    = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE", onupdate="CASCADE"))

    def __init__(self, activity_id, assigned_to, initiated_by):
        self.activity_id    = activity_id
        self.assigned_to    = assigned_to
        self.initiated_by   = initiated_by

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id                  = db.Column(db.Integer, primary_key=True)
    firstname           = db.Column(db.String(64))
    middlename          = db.Column(db.String(64), nullable=True)
    lastname            = db.Column(db.String(64))
    email               = db.Column(db.String(64), unique=True)
    password_hash       = db.Column(db.String(128))
    department          = db.Column(db.String(100))
    position            = db.Column(db.String(100))
    birthday            = db.Column(db.Date)
    role                = db.Column(db.Integer) #0 user #1 admin

    followed            = db.relationship('Follow', foreign_keys=[Follow.follower_id], backref=db.backref('follower', lazy='joined'), lazy='dynamic', passive_deletes=True, passive_updates=True)
    followers           = db.relationship('Follow', foreign_keys=[Follow.following_id], backref=db.backref('followed', lazy='joined'), passive_deletes=True, passive_updates=True)
    membership          = db.relationship('Membership', backref=db.backref('membership', lazy='joined'), lazy='dynamic', passive_deletes=True, passive_updates=True)
    comments            = db.relationship('Comment', backref=db.backref('commented', lazy='joined'), lazy='dynamic', passive_deletes=True, passive_updates=True)
    initated_activity   = db.relationship('Assignment', foreign_keys=[Assignment.initiated_by], backref=db.backref('initiated'), lazy='dynamic', passive_deletes=True, passive_updates=True)
    assigned_activity   = db.relationship('Assignment', foreign_keys=[Assignment.assigned_to], backref=db.backref('assigned'), lazy='dynamic', passive_deletes=True, passive_updates=True)
    activity            = db.relationship('User_Activity', backref=db.backref('guest', lazy='joined'), lazy='dynamic', passive_deletes=True, passive_updates=True)

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

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def to_json(self):
        json_post = {
            'id'            : self.id,
            'firstname'     : self.firstname,
            'middlename'    : self.middlename,
            'lastname'      : self.lastname,
            'email'         : self.email,
            'password_hash' : self.password,
            'department'    : self.department,
            'position'      : self.position,
            'birthday'      : self.birthday,
            'role'          : self.role
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
        role            = json_user.get('role')

        return User(
            firstname=firstname,
            middlename=middlename,
            lastname=lastname,
            email=email,
            password_hash=password,
            department=department,
            position=position,
            birthday=birthday,
            role=role
        )

class Interest_Group(db.Model):
    __tablename__ = 'interest_group'
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(200), unique=True)
    about         = db.Column(db.String(600))
    cover_photo   = db.Column(db.String(200))
    group_icon    = db.Column(db.String(100))

    def __init__(self, name, about, cover_photo, group_icon):
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

class Activity(db.Model):
    __tablename__ = 'activity'
    id            = db.Column(db.Integer, primary_key=True)
    title         = db.Column(db.String(200), unique=True)
    description   = db.Column(db.String(200))
    start_date    = db.Column(db.Date)
    end_date      = db.Column(db.Date)  
    address       = db.Column(db.String(100))
    group_id      = db.Column(db.Integer, nullable=True)

    comments    = db.relationship('Comment', backref=db.backref('comments', lazy='joined'), lazy="dynamic", passive_deletes=True, passive_updates=True)
    schedule    = db.relationship('Schedule', backref=db.backref('schedule', lazy='joined'), lazy="dynamic", passive_deletes=True, passive_updates=True)
    assignment  = db.relationship('Assignment', backref=db.backref('assignment', lazy='joined'), lazy='dynamic', passive_deletes=True, passive_updates=True)
    guests      = db.relationship('User_Activity', backref=db.backref('user_activity', lazy='joined'), lazy='dynamic', passive_deletes=True, passive_updates=True)
    
    def __init__(self, title, description, start_date, end_date, address, group_id=None):
        self.title          = title
        self.description    = description
        self.start_date     = start_date
        self.end_date       = end_date
        self.address        = address
        self.group_id       = group_id

    def __repr__(self):
        return '<Activity %r>' % self.title

    def to_json(self):
        json_post = {
            'id'         : self.id,
            'title'      : self.title,
            'description': self.description,
            'start_date' : self.start_date,
            'end_date'   : self.end_date,
            'address'    : self.address,
            'group_id'   : self.group_id
        }
        return json_post

    @staticmethod
    def from_json(json_activity):
        title       = json_activity.get('title')
        description = json_activity.get('description')
        start_date  = json_activity.get('start_date')
        end_date    = json_activity.get('end_date')
        address     = json_activity.get('address')
        group_id    = json_activity.get('group_id')
        
        return Activity(title=title, description=description, start_date=start_date, end_date=end_date, address=address, group_id=group_id)

class User_Activity(db.Model):
    __tablename__ = 'user_activity'
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    status      = db.Column(db.Integer) #0 interested #1 going

    def __init__(self, user_id, activity_id, status = 0):
        self.user_id = user_id
        self.activity_id = activity_id
        self.status = status #going by default

class Schedule(db.Model):
    __tablename__ = 'schedule'
    id            = db.Column(db.Integer, primary_key=True)
    activity_id   = db.Column(db.Integer, db.ForeignKey('activity.id', ondelete="CASCADE", onupdate="CASCADE"))
    time          = db.Column(db.Time)
    location      = db.Column(db.String(200))

    def __init__(self, activity_id, time, location):
        self.activity_id    = activity_id
        self.time           = time
        self.location       = location

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

