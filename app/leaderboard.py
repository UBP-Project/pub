from flask_login import current_user
from app import db


class leaderboard():

    def joined_activity(value=1):
        user = current_user
        user.points = user.points + value
        db.session.commit()