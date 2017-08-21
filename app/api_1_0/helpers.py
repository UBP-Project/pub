from flask import url_for
from app.models import User, Follow
from app.api_1_0.decorators import run_async
from app import db
from datetime import datetime
import uuid

@run_async
def follow_notif(follower_id, to_follow_id):

    actor = User.query.get(follower_id)

    #send notificaton to the user
    content = "<a href='%s'>%s %s</a> follows you" % (url_for('client.view_profile', id=actor.get_id()), actor.firstname, actor.lastname)
    url = url_for('client.view_profile', id=actor.get_id())

    notif = Notification(user_id=to_follow_id, content=content, url=url)
    db.session.add(notif)

    #send notifcation to the followers of the actor
    followers = Follow.query.filter(following_id=actor.get_id())
    followed_user = User.query.get(to_follow_id)
    print(followed_user)

    for follower in followers:
        content = "<a href='%s'>%s %s</a> follows <a href='%s'>%s %s</a> " % \
            (
                url_for('client.view_profile', id=actor.get_id()),
                actor.firstname,
                actor.lastname,
                url_for('client.view_profile', id=followed_user.get_id()),
                followed_user.firstname,
                followed_user.lastname
            )
        url = url_for('client.view_profile', id=followed_user.get_id())
        notif = Notification(user_id=follower.get_id(), content=content, url=url)
        db.session.add(notif)

    db.session.commit()