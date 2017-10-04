from app.api_1_0 import api
from flask_login import current_user
from app.models import Activity, User, User_Activity,\
    Follow, Membership, Interest_Group, Perks
from sqlalchemy.orm import class_mapper
from flask import jsonify, request
from datetime import datetime, date, time, timedelta


def serialize(model):
    """Transforms a model into a dictionary which can be dumped to JSON."""
    # first we get the names of all the columns on your model
    columns = [c.key for c in class_mapper(model.__class__).columns]
    # then we return their values in a dict
    return dict((c, unicode(getattr(model, c))) for c in columns)


@api.route('/feed')
def feed():
    if 'page' in request.args:
        page = int(request.args.get('page'))
    else:
        page = 1

    start_ts = date.today() - timedelta(days=page)
    if page == 1:
        end_ts = date.today() + timedelta(days=1)
    else:
        end_ts = date.today() - timedelta(days=page - 1)

    return jsonify({
        'new_activities': new_activity(start_ts, end_ts),
        'new_perks': new_perks(start_ts, end_ts),
        'new_groups': new_groups(start_ts, end_ts),
        'new_memberships': membership(start_ts, end_ts)
    })


def new_activity(start_ts, end_ts):
    activities = Activity.query\
        .join(User, User.id == Activity.creator_id)\
        .add_columns(User.id, User.firstname, User.lastname,
                     User.image.label("user_image"),
                     Activity.id.label("act_id"),
                     Activity.image.label("act_image"), Activity.title,
                     Activity.description, Activity.creator_id,
                     Activity.timestamp.label("ts"))\
        .filter(Activity.timestamp > start_ts,
                Activity.timestamp < end_ts)\
        .order_by(Activity.timestamp.desc())
    return [activity_to_json(activity) for activity in activities]


def activity_to_json(item):
    activity = {
        'creator_id': item.creator_id,
        'firstname': item.firstname,
        'lastname': item.lastname,
        'user_image': item.user_image,
        'activity_id': item.act_id,
        'activity_image': item.act_image,
        'activity_title': item.title,
        'activity_description': item.description,
        'timestamp': item.ts
    }
    return activity


def new_groups(start_ts, end_ts):
    groups = Interest_Group.query\
        .filter(Interest_Group.timestamp > start_ts,
                Interest_Group.timestamp < end_ts)\
        .order_by(Interest_Group.timestamp.desc())
    return [group.to_json() for group in groups]


def new_perks(start_ts, end_ts):
    perks = Perks.query\
        .filter(Perks.timestamp > start_ts,
                Perks.timestamp < end_ts)\
        .order_by(Perks.timestamp.desc())
    return [perk.to_json() for perk in perks]


def membership(start_ts, end_ts):
    feed = Follow.query.join(Membership,
                             Membership.user_id == Follow.following_id)\
        .add_columns(Membership.group_id, Membership.timestamp)\
        .join(User, Follow.following_id == User.id)\
        .add_columns(User.firstname, User.lastname, User.id.label("user_id"),
                     User.image.label("user_image"))\
        .join(Interest_Group, Interest_Group.id == Membership.group_id)\
        .add_columns(Interest_Group.name, Interest_Group.id.label("group_id"),
                     Interest_Group.name.label("group_name"),
                     Interest_Group.cover_photo.label("group_cover"),
                     Interest_Group.group_icon.label("group_icon"),
                     Interest_Group.about.label("group_about"))\
        .filter(Follow.follower_id == current_user.get_id(),
                Membership.timestamp > start_ts,
                Membership.timestamp < end_ts)\
        .order_by(Membership.timestamp.desc())\
        .distinct()
    return [membership_to_json(f) for f in feed]


def membership_to_json(feed_item):
    membership = {
        'user_id': feed_item.user_id,
        'user_firstname': feed_item.firstname,
        'user_lastname': feed_item.lastname,
        'user_image': feed_item.user_image,
        'group_name': feed_item.group_name,
        'group_id': feed_item.group_id,
        'group_icon': feed_item.group_icon,
        'group_cover': feed_item.group_cover,
        'group_about': feed_item.group_about,
        'timestamp': feed_item.timestamp
    }
    return membership


def user_activity_feed():
    feed = Follow.query.join(User_Activity,
                             User_Activity.user_id == Follow.following_id)\
        .add_columns(User_Activity.group_id, User_Activity.timestamp)\
        .join(User, Follow.following_id == User.id)\
        .add_columns(User.firstname, User.lastname, User.id.label("user_id"),
                     User.image.label("user_image"))\
        .join(Activity, Activity.id == User_Activity.activity_id)\
        .add_columns(Interest_Group.name, Interest_Group.id.label("group_id"),
                     Interest_Group.name.label("group_name"))\
        .filter(Follow.follower_id == current_user.get_id())\
        .order_by(Membership.timestamp.desc())\
        .distinct()
    return [membership_to_json(f) for f in feed]
