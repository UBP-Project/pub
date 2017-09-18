import json
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from ..forms import LoginForm, GroupMembershipForm
from . import client
from app import db
from app.models import User, Interest_Group, Activity, Membership, Role, Follow, Notification, Notification_EntityType, Notification_Object, Points
from ..auth import is_manager_or_leader
from ..forms import UpdateUserFormClient, PasswordFormClient
from ..utils import flash_errors
from sqlalchemy.sql import func

@client.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template("client/index.html", user=current_user)

@client.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    hasError = False
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not  None and user.verify_password(form.password.data):
            login_user(user)

            if(user.is_administrator()):
                return redirect(url_for('admin.index'))
            else:
                return redirect(request.args.get('next') or url_for('client.index'))
                
        hasError = True
    return render_template("client/views/login.html", form=form, hasError=hasError)

@client.route('/notifications/')
@login_required
def notifications():

    notifs = Notification.query\
        .add_columns(Notification.id, Notification.status, Notification.timestamp, Notification.notification_object_id)\
        .join(Notification_Object)\
        .join(Notification_EntityType)\
        .filter(Notification_Object.status == True)\
        .filter(Notification.notifier_id == current_user.get_id())\
        .add_columns(Notification_EntityType.action, Notification_EntityType.entity)\
        .order_by(Notification.timestamp.desc())\
        .all()

    notifications = jsonify([
            {
                'notification_id'   : notification.id,
                'status'            : notification.status,
                'timestamp'         : notification.timestamp,
                'object_id'         : notification.notification_object_id,
                'action'            : notification.action,
                'entity'            : notification.entity,
                'actors'            : [
                    {
                        'id'           : actor.id,
                        'firstname'    : actor.firstname,
                        'middlename'   : actor.middlename,
                        'lastname'     : actor.lastname,
                        'email'        : actor.email,
                        'department'   : actor.department,
                        'position'     : actor.position,
                        'birthday'     : actor.birthday
                    } for actor in User.query.join(Notification_Change).join(Notification_Object).filter(Notification_Object.id == notification.notification_object_id).filter(Notification_Change.actor_id != current_user.get_id()).all()
                ]
            }
            for notification in notifs
        ])
    print(str(notifications))
    return render_template("client/views/notifications.html", user=current_user, notifications=notifications)

@client.route('/leaderboard')
@login_required
def leaderboard():
    # point_leaders = User.query.order_by(User.desc()).limit(10).all()
    # sample = User.query.join(Points).add_columns(func.sum(Points.value).label('points')).all()

    point_leaders = db.session.query(Points, func.sum(Points.value).label('points'))\
        .join(User)\
        .group_by(Points.user_id)\
        .add_columns(User.id, User.firstname, User.lastname, User.image)\
        .order_by('points DESC')\
        .limit(10)\
        .all()

    # followed_leaders = Follow.query.group_by(Follow.following_id).order_by(Follow.following_id).limit(10).all()
    followed_leaders = db.session.query(Follow, func.count(Follow.following_id).label('total'), Follow.following_id)\
        .join(User, User.id == Follow.following_id)\
        .add_columns(User.id, User.firstname, User.lastname, User.image)\
        .group_by(Follow.following_id).order_by('total DESC').limit(10).all()
        
    # db.session.query(Post, func.count(likes.c.user_id).label('total')).join(likes).group_by(Post).order_by('total DESC')
    return render_template("client/views/leaderboard.html", user=current_user,
        point_leaders=point_leaders, followed_leaders=followed_leaders)

@client.route('/perks/')
@login_required
def perks():
    return render_template("client/perks/perks.html")

@client.route('/perks/create')
@login_required
def create_perks():
    return render_template("client/perks/create.html")

@client.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("client.login"))