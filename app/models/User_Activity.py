from app import db

class User_Activity(db.Model):
    __tablename__ = 'user_activity'
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    status      = db.Column(db.Integer) #0 interested #1 going

    # user = db.relationship('User', back_populates='user_activity')
    # activity = db.relationship('Activity', back_populates='user_activity')
    
    def __init__(self, user_id, activity_id, status = 0):
        self.user_id = user_id
        self.activity_id = activity_id
        self.status = status