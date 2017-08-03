import json
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from ..forms import LoginForm, GroupMembershipForm
from . import client
from app import db
from ..models import User, Interest_Group, Activity, Membership

@client.route('/', methods=['GET', 'POST'])
def index():
    interest_groups = Interest_Group.query.all()
    print(json.dumps(interest_groups))
    # interest_groups[1].isMember = True
    activities = Activity.query.all()
    # print(activities)
    return render_template("views/home.html", interest_groups=interest_groups, activities=activities)

@client.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not  None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('client.index'))
    return render_template("views/login.html", form=form)

@client.route('/profile/')
@login_required
def profile():
    return render_template("user/profile.html", user=current_user)


@client.route('/groups/')
@login_required
def groups():
    groups = Interest_Group.query.all()
    return render_template("group/groups.html", groups=groups)

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
    isMember = True if Membership.query.filter( \
        current_user.get_id()==Membership.user_id,\
        id==Membership.group_id).first() \
        else False
    return render_template('group/group.html', group=group, members=members, user=current_user,\
        isMember=isMember, form=form)

@client.route('/profile/<int:id>')
@login_required
def profile_id(id):
    user = User.query.filter_by(id=id).first()
    if user is not None:
        return render_template("user/profile.html", user=user)
    return rendirect(url_for("client.index"))

@client.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("client.login"))