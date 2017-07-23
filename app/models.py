from . import db

class Interest_Group(db.Model):
    __tablename__ = 'interest_group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, index=True)
    about = db.Column(db.String(1000))
    cover_photo = db.Column(db.String(200))
    group_icon = db.Column(db.String(100))

    def to_json(self):
        json_post = {
            'id': self.id,
            'name': self.name,
            'about': self.about,
            'cover_photo': self.cover_photo,
            'group_icon': self.group_icon
        }
        return json_post

    @staticmethod
    def from_json(json_interest_group):
        name        = json_interest_group.get('name')
        about       = json_interest_group.get('about')
        cover_photo = json_interest_group.get('cover_photo')
        group_icon  = json_interest_group.get('group_icon')
        return Interest_Group(name=name, about=about, cover_photo=cover_photo, group_icon=group_icon)

class Activity(db.Model):
    __tablename__ = 'activity'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, index=True)
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime())

    def to_json(self):
        json_post = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date': self.date
        }
        return json_post

    @staticmethod
    def from_json(json_activity):
        title       = json_activity.get('title')
        description = json_activity.get('description')
        date        = json_activity.get('date')
        return Activity(title=title, description=description, date=date)

