from app import db

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