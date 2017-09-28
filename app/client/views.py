import json
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from ..forms import LoginForm, GroupMembershipForm
from . import client
from app import db
from app.models import User, Interest_Group, Activity, Membership, Role, Follow, Notification, Entity, Notification_Object, Points_Type, Points
from ..auth import is_manager_or_leader
from ..forms import UpdateUserFormClient, PasswordFormClient, CreatePerkForm, UpdatePerkForm
from ..utils import flash_errors
from sqlalchemy.sql import func
from app.notification import Notif
from app.models import Perks
from werkzeug.utils import secure_filename
import uuid
import os
from sqlalchemy import or_

@client.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template("client/index.html", user=current_user)

EMAIL_DOMAIN = 'unionbank.com'
@client.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    hasError = False
    if form.validate_on_submit():
        email = form.email.data
        if '@' not in email: # allows login of emails with @unionbank.com
            email = email + '@' + EMAIL_DOMAIN
        user = User.query.filter_by(email = email).first()
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
    return render_template("client/views/notifications.html")

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
    isManager = User.query\
            .join(Role, Role.id == User.role_id)\
            .filter(Role.name == 'Manager', User.id == current_user.get_id()).first() is not None
    return render_template("client/perks/perks.html", isManager=isManager)

@client.route('/perks/manage')
@login_required
def manage_perks():
    isManager = User.query\
            .join(Role, Role.id == User.role_id)\
            .filter(Role.name == 'Manager', User.id == current_user.get_id()).first() is not None
    return render_template("client/perks/manage.html", isManager=isManager)

@client.route('/perks/create', methods=['GET', 'POST'])
@login_required
def create_perks():
    form = CreatePerkForm()
    if form.validate_on_submit():
        image = form.image.data
        image_filename = secure_filename(image.filename)
        extension = image_filename.rsplit('.', 1)[1].lower()
        image_hashed_filename = str(uuid.uuid4().hex) + '.' + extension
        file_path             = os.path.join('app/static/uploads/perks_images', image_hashed_filename)
        image.save(file_path)

        perk = Perks(
            title=form.title.data,
            description=form.description.data,
            image=image_hashed_filename
        )
        db.session.add(perk)
        db.session.commit()
        return redirect(url_for("client.manage_perks"))
    return render_template("client/perks/create.html", form=form)

@client.route('/perks/<string:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_perk(id):
    form = UpdatePerkForm()
    perk = Perks.query.get_or_404(id)

    if request.method == 'POST' and request.form.get('delete') == 'delete':
        db.session.delete(perk)
        return redirect(url_for('client.perks'))

    if form.validate_on_submit():
        if form.image.data:
            image = form.image.data
            image_filename = secure_filename(image.filename)
            extension = image_filename.rsplit('.', 1)[1].lower()
            image_hashed_filename = str(uuid.uuid4().hex) + '.' + extension
            file_path             = os.path.join('app/static/uploads/perks_images', image_hashed_filename)
            image.save(file_path)
            perk.image = image_hashed_filename
        perk.title = form.title.data
        perk.description = form.description.data
        db.session.commit()
        return redirect(url_for("client.manage_perks"))
    # load activity data to the form
    form.title.data       = perk.title
    form.description.data = perk.description
    return render_template('client/perks/edit.html', form=form, perk=perk)

@client.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("client.login"))