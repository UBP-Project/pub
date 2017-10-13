import json
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from ..forms import LoginForm
from . import client
from app import db
from app.models import User, Interest_Group, Activity, Membership, Role, Follow
from ..auth import is_manager_or_leader
from ..forms import UpdateUserFormClient, PasswordFormClient
from ..utils import flash_errors, is_valid_extension
import os
import uuid
from werkzeug.utils import secure_filename

@client.route('/profile/<uuid(strict=False):id>')
@login_required
def view_profile(id):
    user = User.query.get_or_404(id)
    followers_count = Follow.query.filter(Follow.following_id == id).count()
    following_count = Follow.query.filter(Follow.follower_id == id).count()
    is_following = True if Follow.query.filter(Follow.follower_id == current_user.get_id(),\
        Follow.following_id == user.get_id()).first() is not None else False
            
    return render_template("client/user/profile.html", user=user, current_user=current_user, is_following=is_following, followers_count=followers_count, following_count=following_count)

@client.route('/profile/<uuid(strict=False):id>/edit', methods=['POST', 'GET'])
@login_required
def edit_profile(id):
    form = UpdateUserFormClient()
    user = current_user
    if form.validate_on_submit():
        if form.image.data is not None:
            user.set_image(form.image.data)
        user.firstname  = form.firstname.data,
        user.middlename = form.middlename.data,
        user.lastname   = form.lastname.data, 
        user.email      = form.email.data,
        user.department = form.department.data,
        user.position   = form.position.data,
        user.birthday   = form.birthday.data,
        db.session.commit()
        return redirect(url_for('client.view_profile', id=current_user.get_id()))
    # load the current user info to the form
    form.firstname.data  = user.firstname
    form.middlename.data = user.middlename
    form.lastname.data   = user.lastname
    form.email.data      = user.email
    form.department.data = user.department
    form.position.data   = user.position
    form.birthday.data   = user.birthday
    # flash_errors(form)

    followers_count = Follow.query.filter(Follow.following_id == id).count()
    following_count = Follow.query.filter(Follow.follower_id == id).count()

    if int(id) != int(current_user.get_id()):
        return redirect(url_for('client.index'))
    return render_template('client/user/edit-profile.html', user=current_user, form=form, \
        followers_count=followers_count, following_count=following_count)

@client.route('/profile/<uuid(strict=False):id>/edit-password', methods=['POST', 'GET'])
@login_required
def edit_password(id):
    form = PasswordFormClient()
    user = current_user
    followers_count = Follow.query.filter(Follow.following_id == id).count()
    following_count = Follow.query.filter(Follow.follower_id == id).count()
    if form.validate_on_submit():
        if user.verify_password(form.old_password.data):
            user.password = form.new_password.data
            db.session.commit()
            return redirect(url_for('client.view_profile', id=current_user.get_id()))

    if int(id) != int(current_user.get_id()):
        return redirect(url_for('client.index'))
    return render_template('client/user/edit-password.html', user=current_user, form=form,
        followers_count=followers_count, following_count=following_count)

@client.route('/profile/<uuid(strict=False):id>/followers')
@login_required
def followers(id):
    user = User.query.get_or_404(id)

    # followers_follow = Follow.query.filter(Follow.following_id == id).all()

    followers = user.get_followers()

    following_count = Follow.query.filter(Follow.follower_id == id).count()

    is_following = True if Follow.query.filter(Follow.follower_id == current_user.get_id(),\
        Follow.following_id == user.get_id()).first() is not None else False

    return render_template("client/user/followers.html", user=user, current_user=current_user,\
        is_following=is_following, followers_count=len(followers), following_count=following_count,\
        followers=followers)

@client.route('/profile/<uuid(strict=False):id>/following')
@login_required
def following(id):
    user = User.query.get_or_404(id)

    following_users = Follow.query\
        .join(User, Follow.follower_id == id).all()

    #HARD CODE FIX
    
    followings = []

    for f in following_users:
        followings.append(User.query.get(f.following_id))

    followers_count = Follow.query.filter(Follow.following_id == id).count()

    is_following = True if Follow.query.filter(Follow.follower_id == current_user.get_id(),\
        Follow.following_id == user.get_id()).first() is not None else False

    return render_template("client/user/following.html",\
        user=user,\
        current_user=current_user,\
        is_following=is_following,\
        followers_count=followers_count,\
        followings_count=len(followings),\
        followings=followings)

@client.route('/profile/<uuid(strict=False):id>/points')
@login_required
def points(id):
    user = User.query.get_or_404(id)
    followers_follow = Follow.query.filter(Follow.following_id == id).all()
    followers = []
    for f in followers_follow:
        followers.append(User.query.get(f.follower_id))
    following_count = Follow.query.filter(Follow.follower_id == id).count()
    is_following = True if Follow.query.filter(Follow.follower_id == current_user.get_id(),\
        Follow.following_id == user.get_id()).first() is not None else False
    return render_template("client/user/points.html", user=user, current_user=current_user,\
        is_following=is_following, followers_count=len(followers), following_count=following_count,\
        followers=followers)