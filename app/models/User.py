from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import getpass
from app.models import Role, Permission

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id            = db.Column(db.Integer, primary_key=True)
    firstname     = db.Column(db.String(64))
    middlename    = db.Column(db.String(64), nullable=True)
    lastname      = db.Column(db.String(64))
    email         = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    department    = db.Column(db.String(100))
    position      = db.Column(db.String(100))
    birthday      = db.Column(db.Date)
    role_id       = db.Column(db.Integer, db.ForeignKey('roles.id'))

    # def __init__(self, **kwargs):
    #     super(User, self).__init__(**kwargs)
    #     if self.role is None:
    #         if self.email == 'admin@ubppub.com': # admin
    #             self.role = Role.query.filter_by(permissions=0xffff).first()
    #         if self.role is None:
    #             self.role = Role.query.filter_by(default=True).first()
    #             
    
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
            'password_hash' : self.password_hash,
            'department'    : self.department,
            'position'      : self.position,
            'birthday'      : self.birthday,
            'role_id'       : self.role_id
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