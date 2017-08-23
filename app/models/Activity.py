from app import db
# from app.models.guid import GUID
from sqlalchemy_utils import UUIDType
import uuid


class Activity(db.Model):
    __tablename__ = 'activity'
    id            = db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    title         = db.Column(db.String(200), unique=False) #true on deployment
    description   = db.Column(db.Text(4294967295))
    start_date    = db.Column(db.Date)
    end_date      = db.Column(db.Date)  
    address       = db.Column(db.String(100))
    group_id      = db.Column(UUIDType(binary=False), db.ForeignKey('interest_group.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=True)
    image         = db.Column(db.String(200))

    # comments    = db.relationship('Comment', backref=db.backref('comments', lazy='joined'), lazy="dynamic", passive_deletes=True, passive_updates=True)
    # schedule    = db.relationship('Schedule', backref=db.backref('schedule', lazy='joined'), lazy="dynamic", passive_deletes=True, passive_updates=True)
    # assignment  = db.relationship('Assignment', backref=db.backref('assignment', lazy='joined'), lazy='dynamic', passive_deletes=True, passive_updates=True)
    # guests      = db.relationship('User_Activity', backref=db.backref('user_activity', lazy='joined'), lazy='dynamic', passive_deletes=True, passive_updates=True)
    
    def __init__(self, title, description, start_date, end_date, address, group_id, image):
        self.title       = title
        self.description = description
        self.start_date  = start_date
        self.end_date    = end_date
        self.address     = address
        self.group_id    = group_id or None
        self.image       = image

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
        image       = json_activity.get('image')
        
        return Activity(title=title, description=description, start_date=start_date, end_date=end_date, address=address, group_id=group_id, image=image)