import json
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from ..forms import LoginForm, GroupMembershipForm
from . import client
from app import db
from app.models import User, Interest_Group, Activity, Membership, Role, Follow
from ..auth import manager_or_leader_only
from ..forms import UpdateUserFormClient, PasswordFormClient
from ..utils import flash_errors

@client.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template("client/views/home.html", user=current_user)

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
    return render_template("client/views/notifications.html", user=current_user)

@client.route('/leaderboard')
@login_required
def leaderboard():
    point_leaders = User.query.order_by(User.points.desc()).limit(10).all()
    return render_template("client/views/leaderboard.html", user=current_user,
        point_leaders=point_leaders)

@client.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("client.login"))