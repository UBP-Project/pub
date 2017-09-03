from flask_login import current_user
from app import db


class leaderboard():
    @staticmethod
    def joined_activity(user=current_user, value=1):
        user.points = user.points + value
        db.session.commit()