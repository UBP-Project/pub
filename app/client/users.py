import json
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from ..forms import LoginForm
from . import client
from app import db
from app.models import User, Interest_Group, Activity, Membership, Role, Follow
from ..auth import manager_or_leader_only
from ..forms import UpdateUserFormClient, PasswordFormClient
from ..utils import flash_errors

@client.route('/profile/<int:id>')
@login_required
def view_profile(id):
    user = User.query.get_or_404(id)
    is_following = True if Follow.query.filter(Follow.follower_id == current_user.get_id(),\
        Follow.following_id == user.get_id()).first() is not None else False
    return render_template("client/views/profile.html", user=user, current_user=current_user, is_following=is_following)

@client.route('/profile/<int:id>/edit', methods=['POST', 'GET'])
@login_required
def edit_profile(id):
    form = UpdateUserFormClient()
    user = current_user
    if form.validate_on_submit():
        print('Validated')
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

    if int(id) != int(current_user.get_id()):
        return redirect(url_for('client.index'))
    return render_template('client/views/edit-profile.html', user=current_user, form=form)

@client.route('/profile/<int:id>/edit-password', methods=['POST', 'GET'])
@login_required
def edit_password(id):
    form = PasswordFormClient()
    user = current_user
    if form.validate_on_submit():
        if user.verify_password(form.old_password.data):
            user.password = form.new_password.data
            db.session.commit()
            return redirect(url_for('client.view_profile', id=current_user.get_id()))

    if int(id) != int(current_user.get_id()):
        return redirect(url_for('client.index'))
    return render_template('client/views/edit-password.html', user=current_user, form=form)

@client.route('/profile/<int:id>/followers')
@login_required
def followers(id):
    return "Followers"

@client.route('/profile/<int:id>/following')
@login_required
def following(id):
    return "Following"

@client.route('/self')
@login_required
def self():
    return current_user.get_id();