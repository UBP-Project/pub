from app import db

class User(db.Model):
    __tablename__ = 'user'
    id            = db.Column(db.Integer, primary_key=True)
    firstname     = db.Column(db.String(200))
    middlename    = db.Column(db.String(200))
    lastname      = db.Column(db.String(200))
    email         = db.Column(db.String(100))
    password      = db.Column(db.String(100))
    department    = db.Column(db.String(200))
    position      = db.Column(db.String(200))
    birthday      = db.Column(db.Date)

    comments      = db.relationship('Comment', backref='user')

    def to_json(self):
        json_post = {
            'id'        : self.id,
            'firstname' : self.firstname,
            'middlename': self.middlename,
            'lastname'  : self.lastname,
            'email'     : self.email,
            'password'  : self.password,
            'department': self.department,
            'position'  : self.position,
            'birthday'  : self.birthday
        }
        return json_post

    @staticmethod
    def from_json(json_user):
        firstname   = json_user.get('firstname')
        middlename  = json_user.get('middlename')
        lastname    = json_user.get('lastname')
        email       = json_user.get('email')
        password    = json_user.get('password')
        department  = json_user.get('department')
        position    = json_user.get('position')
        birthday    = json_user.get('birthday')

        return User(
            firstname=firstname,
            middlename=middlename,
            lastname=lastname,
            email=email,
            password=password,
            department=department,
            position=position,
            birthday=birthday
        )


class Follow(db.Model):
    __tablename__ = 'follow'
    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer)
    following_id  = db.Column(db.Integer)
    follow_date   = db.Column(db.Date)


class Interest_Group(db.Model):
    __tablename__ = 'interest_group'
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(200), unique=True, index=True)
    about         = db.Column(db.String(1000))
    cover_photo   = db.Column(db.String(200))
    group_icon    = db.Column(db.String(100))

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
    id                = db.Column(db.Integer, primary_key=True)
    user_id           = db.Column(db.Integer)
    group_id          = db.Column(db.Integer)
    date_joined       = db.Column(db.Date)
    membership_status = db.String(db.String(20)) # 'pending', 'accepted', 'declined'
    membership_level  = db.Column(db.String(20)) # 'admin' or 'regular' member


class Activity(db.Model):
    __tablename__ = 'activity'
    id            = db.Column(db.Integer, primary_key=True)
    title         = db.Column(db.String(200), unique=True, index=True)
    description   = db.Column(db.String(200))
    start_date    = db.Column(db.Date)
    end_date      = db.Column(db.Date)
    address       = db.Column(db.String(200))

    def to_json(self):
        json_post = {
            'id'         : self.id,
            'title'      : self.title,
            'description': self.description,
            'start_date' : self.start_date,
            'end_date'   : self.end_date
        }
        return json_post

    @staticmethod
    def from_json(json_activity):
        title       = json_activity.get('title')
        description = json_activity.get('description')
        start_date  = json_activity.get('start_date')
        end_date    = json_activity.get('end_date')
        return Activity(title=title, description=description, start_date=start_date, end_date=end_date)


class User_Activity(db.Model):
    __tablename__ = 'user_activity'
    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer)
    activity_id   = db.Column(db.Integer)
    status        = db.Column(db.String(50))


class Activity_Schedule(db.Model):
    __tablename__ = 'activity_schedule'
    id            = db.Column(db.Integer, primary_key=True)
    activity_id   = db.Column(db.Integer)
    time          = db.Column(db.Time)
    location      = db.Column(db.String(200))

class Comment(db.Model):
    __tablename__ = 'comment'
    id            = db.Column(db.Integer, primary_key=True)
    text          = db.Column(db.String(300))
    timestamp     = db.Column(db.Time) #set default to system's current time
    user_id       = db.column(db.Integer, db.ForeignKey('user.id'))
    activity_id   = db.column(db.Integer) 