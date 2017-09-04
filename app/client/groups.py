import json
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from . import client
from app import db
from app.models import User, Interest_Group, Activity, Membership, Role, Follow
from ..auth import manager_or_leader_only
from ..utils import flash_errors

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
        .paginate(page = 1 , per_page = 12, error_out=False).items
    managed_groups = Interest_Group.query.join(Membership,\
        Membership.group_id == Interest_Group.id).filter(Membership.level == 1,\
        Membership.user_id == current_user.get_id()).all()
    return render_template("client/views/groups.html", interest_groups=interest_groups, managed_groups=managed_groups, user=current_user)

@client.route('/groups/<uuid(strict=False):id>', methods=['POST', 'GET'])
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

@client.route('/groups/<uuid(strict=False):id>/requests', methods=['POST', 'GET'])
@login_required
def group_requests(id):
    manager_or_leader_only(id) # check if the current user is a manager or leader
    group = Interest_Group.query.get_or_404(id)
    membership_requests = User.query \
        .join(Membership, User.id==Membership.user_id) \
        .filter(Membership.group_id==id, Membership.status == 0, Membership.level == 0).all()
    return render_template('client/views/group-requests.html', group=group, membership_requests=membership_requests)
