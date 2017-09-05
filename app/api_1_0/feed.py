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
    feed = Follow.query.join(Membership, Membership.user_id == Follow.following_id)\
        .add_columns(Membership.group_id, Membership.date_joined)\
        .join(User, Follow.following_id == User.id)\
        .add_columns(User.firstname, User.id.label("user_id"))\
        .join(Interest_Group, Interest_Group.id == Membership.group_id)\
        .add_columns(Interest_Group.name, Interest_Group.id.label("group_id"))\
        .filter(Follow.follower_id == current_user.get_id())\
        .order_by(Membership.date_joined.desc())\
        .distinct()
    return jsonify({
        'feed': [membership_to_json(f) for f in feed]
    })

def membership_to_json(feed_item):
    membership = {
        'user_firstname'  : feed_item.firstname,
        'user_date_joined': feed_item.date_joined,
        'group_name'      : feed_item.name,
        'group_id'        : feed_item.group_id,
        'user_id'         : feed_item.user_id
    }
    return membership
