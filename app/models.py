from . import db

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
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer)
    group_id    = db.Column(db.Integer)
    date_joined = db.Column(db.Date)
    status      = db.String(db.String(20)) # 'pending', 'accepted', 'declined'
    level       = db.Column(db.String(20)) # 'admin' or 'regular' member


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
            'start_date' : self.date,
            'end_date'   : self.end_date
        }
        return json_post

    @staticmethod
    def from_json(json_activity):
        title       = json_interest_group.get('title')
        description = json_interest_group.get('description')
        date        = json_interest_group.get('date')
        return Activity(title=title, description=description, date=date)


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
