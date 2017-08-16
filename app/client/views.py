import json
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from ..forms import LoginForm, GroupMembershipForm
from . import client
from app import db
from app.models import User, Interest_Group, Activity, Membership, Role, Follow
from ..auth import manager_or_leader_only

@client.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template("client/views/home.html")

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

@client.route('/profile/')
@login_required
def profile():
    return render_template("user/profile.html", user=current_user)

@client.route('/activities/')
@login_required
def activities():
    activities = Activity.query.limit(7)
    return render_template("client/views/activities.html", activities=activities)

@client.route('/groups/')
@login_required
def groups():

    #problem still exist in this query
    interest_groups = Interest_Group.query  \
        .outerjoin(Membership) \
        .outerjoin(User) \
        .with_entities(
            Interest_Group.id,              \
            Interest_Group.name,            \
            Interest_Group.about,           \
            Interest_Group.cover_photo,     \
            Interest_Group.group_icon,      \
            Membership.status
            )  \
        .limit(14)    

    managed_groups = Interest_Group.query.join(Membership,\
        Membership.group_id == Interest_Group.id).filter(Membership.level == 1,\
        Membership.user_id == current_user.get_id()).all()

    return render_template("client/views/groups.html", interest_groups=interest_groups, managed_groups=managed_groups)

@client.route('/groups/<int:id>', methods=['POST', 'GET'])
@login_required
def group(id):
    form = GroupMembershipForm()
    # handle page actions
    if form.validate_on_submit():
        if form.join_group.data:
            membership = Membership(
                user_id=current_user.get_id(),
                group_id=id,
                status=1,
                level='regular')
            db.session.add(membership)
            db.session.commit()
        else:
            Membership.query.filter(\
                Membership.user_id==current_user.get_id(),
                Membership.group_id==id).delete()

    # query page data
    group = Interest_Group.query.get_or_404(id)
    members = User.query \
        .join(Membership, User.id==Membership.user_id) \
        .filter(Membership.group_id==id, Membership.status != 0)
    membership = Membership.query.filter( \
        current_user.get_id()==Membership.user_id,\
        id==Membership.group_id).first()
    return render_template('client/views/group.html', group=group, members=members, user=current_user,\
        membership=membership, form=form)

@client.route('/groups/<int:id>/requests', methods=['POST', 'GET'])
@login_required
def group_requests(id):
    manager_or_leader_only(id) # check if the current user is a manager or leader
    group = Interest_Group.query.get_or_404(id)
    membership_requests = User.query \
        .join(Membership, User.id==Membership.user_id) \
        .filter(Membership.group_id==id, Membership.status == 0, Membership.level == 0).all()
    return render_template('client/views/group-requests.html', group=group, membership_requests=membership_requests)

@client.route('/profile/<int:id>')
@login_required
def profile_id(id):
    user = User.query.get_or_404(id)
    is_following = True if Follow.query.filter(Follow.follower_id == current_user.get_id(),\
        Follow.following_id == user.get_id()).first() is not None else False
    print(is_following)
    return render_template("client/views/profile.html", user=user, current_user=current_user, is_following=is_following)

@client.route('/profile/<int:id>/edit')
@login_required
def edit_profile(id):
    print(id, current_user.get_id())
    if int(id) != int(current_user.get_id()):
        return redirect(url_for('client.index'))
    return render_template('client/views/edit-profile.html', user=current_user)

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

@client.route('/notifications/')
@login_required
def notifications():
    return render_template("client/views/notifications.html")

@client.route('/settings/')
@login_required
def settings():
    return render_template("client/views/settings.html")

@client.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("client.login"))