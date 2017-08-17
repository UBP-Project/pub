from app import db

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