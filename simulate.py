from app.models import Interest_Group, User, Role, Follow, \
    User_Activity, Activity, Membership, Points_Type, Perks
from app.notification import Notif
import random
from app import db
from datetime import datetime
from random import randrange
import time

random.seed(datetime.now())


def follow(count=20):
    users = User.query.join(Role).filter(Role.name != 'Administrator').all()
    for user in users:
        for i in range(0, count):
            to_follow = users[random.randint(0, len(users) - 1)]
            if to_follow == user:
                continue

            exists = Follow.query.filter(Follow.follower_id == user.get_id(
            ), Follow.following_id == to_follow.get_id()).first() is not None

            if exists:
                continue
            else:
                notification = Notif('user', 'followed', to_follow.get_id())
                notification.add_actor(user.get_id())

                follow = Follow(follower_id=user.get_id(),
                                following_id=to_follow.get_id())
                db.session.add(follow)

                print(user.firstname, user.lastname, "followed",
                      to_follow.firstname, to_follow.lastname)
    db.session.commit()


def activity_join(activity_count=10, user_count=100):
    users = User.query.join(Role).filter(Role.name != 'Administrator').all()
    activities = Activity.query.all()
    for i in range(0, user_count):
        user = users[random.randint(0, len(users) - 1)]
        for j in range(0, activity_count):
            activity = activities[random.randint(0, len(activities) - 1)]
            user_activity = User_Activity(user_id=user.id,
                                          activity_id=activity.id, status=[1])
            exists = User_Activity.query.filter_by(user_id=user.get_id(),
                                                   activity_id=activity.id).first() is not None
            if exists:
                continue
            else:
                notification = Notif('activity', 'going', activity.id)
                notification.add_actor(user.id)

                user.earn_point('Joined %s' % activity.title,
                                'activity', activity.id, 'going')
                db.session.add(user_activity)

                print(user.firstname, user.lastname,
                      "is going to", activity.title)
    db.session.commit()


def activity_interested(activity_count=10, user_count=100):
    users = User.query.join(Role).filter(Role.name != 'Administrator').all()
    activities = Activity.query.all()
    for i in range(0, user_count):
        user = users[random.randint(0, len(users) - 1)]
        for j in range(0, activity_count):
            activity = activities[random.randint(0, len(activities) - 1)]
            user_activity = User_Activity(user_id=user.id,
                                          activity_id=activity.id, status=[0])
            exists = User_Activity.query.filter_by(user_id=user.get_id(),
                                                   activity_id=activity.id).first() is not None
            if exists:
                continue
            else:
                notification = Notif('activity', 'interested', activity.id)
                notification.add_actor(user.id)
                db.session.add(user_activity)
                print(user.firstname, user.lastname,
                      "is interested in", activity.title)
    db.session.commit()


def join_group(group_count=5, user_count=100):
    users = User.query.join(Role).filter(Role.name != 'Administrator').all()
    groups = Interest_Group.query.all()
    for i in range(0, user_count):
        user = users[random.randint(0, len(users) - 1)]
        for j in range(0, group_count):
            group = groups[random.randint(0, len(groups) - 1)]
            membership = Membership(
                user_id=user.id,
                group_id=group.id,
                status=1,
                level=0)
            exists = Membership.query.filter_by(user_id=user.id,
                                                group_id=group.id).first() is not None
            if exists:
                continue
            else:
                db.session.add(membership)
                user.earn_point(
                    'Joined %s' % group.name, 'interest_group', group.id, 'accepted_join_request')
                print(user.firstname, user.lastname,
                      "joins group: ", group.name)
    db.session.commit()


def join_group_pending(group_count=5, user_count=100):
    users = User.query.join(Role).filter(Role.name != 'Administrator').all()
    groups = Interest_Group.query.all()
    for i in range(0, user_count):
        user = users[random.randint(0, len(users) - 1)]
        for j in range(0, group_count):
            group = groups[random.randint(0, len(groups) - 1)]
            membership = Membership(
                user_id=user.id,
                group_id=group.id,
                status=0,
                level=0)
            exists = Membership.query.filter_by(user_id=user.id,
                                                group_id=group.id).first() is not None
            if exists:
                continue
            else:
                db.session.add(membership)
                print(user.firstname, user.lastname,
                      "pending joins group: ", group.name)
    db.session.commit()


def group_activities(group_count=10, activity_count=3):
    groups = Interest_Group.query.all()
    activities = Activity.query.all()
    for i in range(0, group_count):
        group = groups[random.randint(0, len(groups) - 1)]
        for j in range(0, activity_count):
            activity = activities[random.randint(0, len(activities) - 1)]
            activity.group_id = group.id
    db.session.commit()


""" 
Give random time given the range
"""
def randomize_time(start_timestamp,end_timestamp):
    return time.localtime(randrange(start_timestamp,end_timestamp))

"""
    Modify timestamps of certain records to simulate realistic user actions
"""
def modify_timestamps():

    print("Modifying timestamps")
    
    start_timestamp = time.mktime(time.strptime('Sep 1 2017  01:33:00', '%b %d %Y %I:%M:%S'))
    end_timestamp = time.mktime(time.strptime('Oct 12 2017  08:33:00', '%b %d %Y %I:%M:%S'))

    follows = Follow.query.all()
    for follow in follows:
        follow.timestamp = randomize_time(start_timestamp, end_timestamp)

    activities = Activity.query.all()
    for activity in activities:
        activity.timestamp = randomize_time(start_timestamp, end_timestamp)

    groups = Interest_Group.query.all()
    for group in groups:
        group.timestamp = randomize_time(start_timestamp, end_timestamp)


    perks = Perks.query.all()
    for perk in perks:
        perk.timestamp = randomize_time(start_timestamp, end_timestamp)

    memberships = Membership.query.all()
    for membership in memberships:
        membership.timestamp = randomize_time(start_timestamp, end_timestamp)

    user_activities = User_Activity.query.all()
    for user_activity in user_activities:
        user_activity.timestamp = randomize_time(start_timestamp, end_timestamp)

    db.session.commit()


def all():
    activity_join()
    activity_interested()
    join_group()
    join_group_pending()
    follow()
    # group_activities()
    modify_timestamps()


