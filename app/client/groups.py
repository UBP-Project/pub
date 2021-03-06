import json
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_required
from . import client
from app import db
from app.models import User, Interest_Group, Activity, Membership, Role, Follow
from ..auth import is_manager_or_leader, is_manager, can_modify_group, can_accept_requests
from ..utils import flash_errors, is_valid_extension
from ..forms import CreateInterestGroupForm, UpdateInterestGroupForm, GroupMembershipForm
from werkzeug.utils import secure_filename
import os
import uuid

@client.route('/groups')
@login_required
def groups():
    return render_template("client/group/groups.html", user=current_user, is_manager=is_manager())

@client.route('/groups/<uuid(strict=False):id>', methods=['POST', 'GET'])
@login_required
def group(id):
    activities = Activity.query.filter(Activity.group_id == id).all()
    form = GroupMembershipForm()
    # handle page actions
    if form.validate_on_submit():
        if form.join_group.data:
            membership = Membership(
                user_id=current_user.get_id(),
                group_id=id,
                status=1,
                level=0)
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
    return render_template('client/group/group.html', group=group, members=members, user=current_user,\
        membership=membership, form=form, activities=activities, can_manage_activity = is_manager_or_leader(), is_manager = is_manager())

@client.route('/groups/<string:id>/edit', methods=['GET', 'POST'])
def update_group(id):
    #can_modify_group(id, abort_on_false=True)
    form = UpdateInterestGroupForm()
    group = Interest_Group.query.get_or_404(id)

    if request.method == 'POST' and request.form.get('delete') == 'delete':
        db.session.delete(group)
        return redirect(url_for('admin.groups'))

    if form.validate_on_submit():
        # handle upload group cover
        if form.cover_photo.data is not None:
            cover = form.cover_photo.data
            group.set_cover(cover)

        # handle upload user icon
        if form.group_icon.data is not None:
            icon = form.group_icon.data
            group.set_icon(icon)

        group.name = form.name.data
        group.about = form.about.data
        db.session.commit()

        # edit group points
        group.edit_points('accepted_join_request', form.joined_point.data)

        return redirect(url_for('client.group', id=id))
    form.name.data = group.name
    form.about.data = group.about
    form.joined_point.data = group.get_points('accepted_join_request')
    return render_template('client/group/edit.html', form=form, group=group)


@client.route('/groups/create', methods=['POST', 'GET'])
@login_required
# manager_only
def create_group():
    is_manager(abort_on_false=True) # 403 -Forbiden if not a manager
    form = CreateInterestGroupForm()
    if form.validate_on_submit():
        interest_group = Interest_Group(
            name=form.name.data,
            about=form.about.data)
        db.session.add(interest_group)
        db.session.commit()

        # set images
        interest_group.set_icon(form.group_icon.data)
        interest_group.set_cover(form.cover_photo.data)

        # set points
        interest_group.set_points('accepted_join_request', form.joined_point.data)

        # insert leaders
        leader_ids = form.leader_ids.data.split(',')
        interest_group.set_leaders(leader_ids)

        # set manager of group via membership
        membership = Membership(
            user_id=current_user.get_id(),
            group_id=interest_group.id,
            status=1,
            level=2 # 2 is manager level
        )
        db.session.add(membership)
        db.session.commit()
        return redirect(url_for("client.group", id=interest_group.id))
    return render_template('client/group/create.html', form=form)

@client.route('/mygroups/')
@login_required
def mygroups():
    return render_template("client/group/mygroups.html", user=current_user, is_manager=is_manager())

@client.route('/groups/<uuid(strict=False):id>/requests', methods=['POST', 'GET'])
@login_required
def group_requests(id):
    is_manager_or_leader(abort_on_false=True) # check if the current user is a manager or leader
    group = Interest_Group.query.get_or_404(id)
    membership_requests = User.query \
        .join(Membership, User.id==Membership.user_id) \
        .filter(Membership.group_id==id, Membership.status == 0, Membership.level == 0).all()
    return render_template('client/group/requests.html', group=group, membership_requests=membership_requests,
        can_edit_group=can_modify_group(id), can_accept_requests=can_accept_requests(id))

@client.route('/groups/<string:id>/members', methods=['GET', 'POST'])
def group_members(id):
    group = Interest_Group.query.get_or_404(id)
    return render_template('client/group/members.html', group=group, 
        can_edit_group=can_modify_group(id), can_accept_requests=can_accept_requests(id))

@client.route('/groups-list')
def group_list():
    groups = Interest_Group.query.all()
    return jsonify({
        'groups': [ {
            'group_id': group.id
        } for group in groups ]
    }), 200
