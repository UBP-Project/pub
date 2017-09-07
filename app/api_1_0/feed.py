from app.api_1_0 import api
from flask_login import current_user
from app.models import Activity, User, User_Activity, Follow, Membership, Interest_Group
import json
from sqlalchemy.orm import class_mapper
from flask import render_template, jsonify
from pprint import pprint

def serialize(model):
  """Transforms a model into a dictionary which can be dumped to JSON."""
  # first we get the names of all the columns on your model
  columns = [c.key for c in class_mapper(model.__class__).columns]
  # then we return their values in a dict
  return dict((c, unicode(getattr(model, c))) for c in columns)

@api.route('/feed')
def feed():
    return membership_feed()

def membership_feed():
    feed = Follow.query.join(Membership, Membership.user_id == Follow.following_id)\
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
        .filter(Follow.follower_id == current_user.get_id())\
        .order_by(Membership.timestamp.desc())\
        .distinct()
    return jsonify({
        'feed': [membership_to_json(f) for f in feed]
    })

# def user_activity_feed():
#     feed = Follow.query.join(User_Activity, User_Activity.user_id == Follow.following_id)\
#         .add_columns(User_Activity.group_id, User_Activity.timestamp)\
#         .join(User, Follow.following_id == User.id)\
#         .add_columns(User.firstname, User.lastname, User.id.label("user_id"),
#             User.image.label("user_image"))\
#         .join(Activity, Activity.id == User_Activity.activity_id)\
#         .add_columns(Interest_Group.name, Interest_Group.id.label("group_id"),
#             Interest_Group.name.label("group_name"))\
#         .filter(Follow.follower_id == current_user.get_id())\
#         .order_by(Membership.timestamp.desc())\
#         .distinct()
#     return jsonify({
#         'feed': [membership_to_json(f) for f in feed]
#     })

def membership_to_json(feed_item):
    membership = {
        'type'          : 'group_membership',
        'user_id'       : feed_item.user_id,
        'user_firstname': feed_item.firstname,
        'user_lastname' : feed_item.lastname,
        'user_image'    : feed_item.user_image,
        'group_name'    : feed_item.group_name,
        'group_id'      : feed_item.group_id,
        'group_icon'    : feed_item.group_icon,
        'group_cover'   : feed_item.group_cover,
        'group_about'   : feed_item.group_about,
        'timestamp'     : feed_item.timestamp
    }
    return membership
