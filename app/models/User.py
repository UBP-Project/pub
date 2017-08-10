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
    # role                = db.Column(db.Integer) #0 user #1 admin

    # followed            = db.relationship('Follow', foreign_keys=[Follow.follower_id], backref=db.backref('follower', lazy='joined'), lazy='dynamic', passive_deletes=True, passive_updates=True)
    # followers           = db.relationship('Follow', foreign_keys=[Follow.following_id], backref=db.backref('followed', lazy='joined'), passive_deletes=True, passive_updates=True)
    membership          = db.relationship('Membership', backref=db.backref('membership', lazy='joined'), lazy='dynamic', passive_deletes=True, passive_updates=True)
    # comments            = db.relationship('Comment', backref=db.backref('commented', lazy='joined'), lazy='dynamic', passive_deletes=True, passive_updates=True)
    # initated_activity   = db.relationship('Assignment', foreign_keys=[Assignment.initiated_by], backref=db.backref('initiated'), lazy='dynamic', passive_deletes=True, passive_updates=True)
    # assigned_activity   = db.relationship('Assignment', foreign_keys=[Assignment.assigned_to], backref=db.backref('assigned'), lazy='dynamic', passive_deletes=True, passive_updates=True)
    # user_activity            = db.relationship('User_Activity', uselist = False, back_populates='user')


    # def __init__(self, **kwargs):
    #     super(User, self).__init__(**kwargs)
    #     if self.role is None:
    #         if self.email == 'admin@ubppub.com': # admin
    #             self.role = Role.query.filter_by(permissions=0xffff).first()
    #         if self.role is None:
    #             self.role = Role.query.filter_by(default=True).first()
    #             
    
    @staticmethod
    def create_admin():
        email = input('Admin Email: ')
        password = getpass.getpass('Password:  ')
        admin_role = Role.query.filter(Role.name == "Administrator").first()
        admin = User(email=email, password=password, role_id=admin_role.id)
        try:
            db.session.add(admin)
            db.session.commit()
            print("Administrator account created.")
            print("You can login on https://[host]/login")
            print("and view admin pages in https://[host]/admin")
        except:
            print("Unable to created administrator account.")
            print("Make sure that the database is connected and the tables are present.")

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
            'role'          : self.role
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