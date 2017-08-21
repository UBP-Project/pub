from app import db
from app.models import Follow, User

following = User.query.filter(User.firstname =='test').first()
followers = User.query.filter(User.id != following.get_id()).all()

for f in followers:
	follow = Follow(follower_id=f.get_id(), following_id=following.get_id())
	db.session.add(follow)
db.session.commit()