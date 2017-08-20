from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from app.models import Role, Permission
# from app.models.guid import GUID
from sqlalchemy_utils import UUIDType
from flask_login import UserMixin
import uuid
import getpass
from uuid import UUID


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

@login_manager.user_loader
def load_user(user_id):
    if type(user_id) is str:
        print("Is STR")
        return None
    return User.query.get(user_id)