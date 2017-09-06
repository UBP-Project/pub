from flask import render_template, flash, redirect, url_for, request
from .. import admin
from ...forms import CreateInterestGroupForm, UpdateInterestGroupForm
from app import db
from app.models import User, Interest_Group, Membership, Activity
from ...decorators import admin_required
from ...utils import flash_errors, is_valid_extension
from werkzeug.utils import secure_filename
import os
import uuid
from flask_login import current_user
from app.notification.Notif import Notif

@admin.route('/groups')
@admin_required
def groups():
    groups = Interest_Group.query.all()
    return render_template('admin/group/groups.html', groups=groups)

@admin.route('/groups/<string:id>', methods=['GET', 'POST'])
@admin_required
def group(id):
    group = Interest_Group.query.get_or_404(id)
    activities = Activity.query.filter(Activity.group_id == id).all()
    leaders = User.query \
        .join(Membership, User.id==Membership.user_id) \
        .filter(Membership.group_id==id, Membership.status != 0, Membership.level == 1)
    members = User.query \
        .join(Membership, User.id==Membership.user_id) \
        .filter(Membership.group_id==id, Membership.status != 0, Membership.level == 0)
    return render_template('admin/group/group.html', group=group, leaders=leaders, members=members, activities=activities)

@admin.route('/groups/create', methods=['GET', 'POST'])
@admin_required
def create_group():
    form = CreateInterestGroupForm()
    if form.validate_on_submit():
        # handle upload group cover
        cover                 = form.cover_photo.data
        cover_filename        = secure_filename(cover.filename)
        extension             = cover_filename.rsplit('.', 1)[1].lower()
        cover_hashed_filename = str(uuid.uuid4().hex) + '.' + extension
        file_path             = os.path.join('app/static/uploads/covers', cover_hashed_filename)
        cover.save(file_path)

        # handle upload user icon
        icon                 = form.group_icon.data
        icon_filename        = secure_filename(icon.filename)
        extension            = icon_filename.rsplit('.', 1)[1].lower()
        icon_hashed_filename = str(uuid.uuid4().hex) + '.' + extension
        file_path            = os.path.join('app/static/uploads/group_icons', icon_hashed_filename)
        icon.save(file_path)

        interest_group = Interest_Group(
            name=form.name.data,
            about=form.about.data,
            cover_photo=cover_hashed_filename,
            group_icon=icon_hashed_filename)
        db.session.add(interest_group)
        db.session.commit()
        return redirect(url_for("admin.groups"))
    return render_template('admin/group/create.html', form=form)

@admin.route('/groups/<string:id>/edit', methods=['GET', 'POST'])
@admin_required
def update_group(id):
    form = UpdateInterestGroupForm()
    group = Interest_Group.query.get_or_404(id)

    if request.method == 'POST' and request.form.get('delete') == 'delete':
        db.session.delete(group)
        return redirect(url_for('admin.groups'))

    if form.validate_on_submit():
        # handle upload group cover
        if form.cover_photo.data is not None:
            cover                 = form.cover_photo.data
            cover_filename        = secure_filename(cover.filename)
            if is_valid_extension(cover_filename):
                extension             = cover_filename.rsplit('.', 1)[1].lower()
                cover_hashed_filename = str(uuid.uuid4().hex) + '.' + extension
                file_path             = os.path.join('app/static/uploads/covers', cover_hashed_filename)
                cover.save(file_path)
                group.cover_photo = cover_hashed_filename

        # handle upload user icon
        if form.group_icon.data is not None:
            icon                 = form.group_icon.data
            icon_filename        = secure_filename(icon.filename)
            if is_valid_extension(icon_filename):
                extension            = icon_filename.rsplit('.', 1)[1].lower()
                icon_hashed_filename = str(uuid.uuid4().hex) + '.' + extension
                file_path            = os.path.join('app/static/uploads/group_icons', icon_hashed_filename)
                icon.save(file_path)
                group.group_icon = icon_hashed_filename

        group.name = form.name.data
        group.about = form.about.data
        db.session.commit()
        return redirect(url_for('admin.group', id=id))
    form.name.data = group.name
    form.about.data = group.about
    return render_template('admin/group/edit.html', form=form, group=group)


# Actions
@admin.route('/groups/setleader/<string:group_id>/<string:user_id>')
@admin_required
def setleader(group_id, user_id):
    membership = Membership.query.filter(Membership.group_id == group_id, Membership.user_id == user_id).first()
    membership.level = 1
    db.session.commit()
    return redirect(url_for("admin.group_members", id=group_id))

@admin.route('/removeleader/<string:group_id>/<string:user_id>')
@admin_required
def removeleader(group_id, user_id):
    membership = Membership.query.filter(Membership.group_id == group_id, Membership.user_id == user_id).first()
    membership.level = 0
    db.session.commit()
    return redirect(url_for("admin.group_members", id=group_id))

@admin.route('/groups/<string:id>/members', methods=['GET', 'POST'])
@admin_required
def group_members(id):
    group = Interest_Group.query.get_or_404(id)
    leaders = User.query \
        .join(Membership, User.id==Membership.user_id) \
        .filter(Membership.group_id==id, Membership.status != 0, Membership.level == 1).all()
    members = User.query \
        .join(Membership, User.id==Membership.user_id) \
        .filter(Membership.group_id==id, Membership.status != 0, Membership.level == 0).all()
    return render_template('admin/group/members.html', group=group, leaders=leaders, members=members)

@admin.route('/groups/<string:id>/requests', methods=['GET', 'POST'])
@admin_required
def group_requests(id):
    group = Interest_Group.query.get_or_404(id)
    membership_requests = User.query \
        .join(Membership, User.id==Membership.user_id) \
        .filter(Membership.group_id==id, Membership.status == 0, Membership.level == 0).all()
    return render_template('admin/group/requests.html', group=group, membership_requests=membership_requests)

@admin.route('/accept_request/<string:group_id>/<string:user_id>')
@admin_required
def accept_request(group_id, user_id):

    #Notification
    notification = Notif('interest_group', 'accepted_join_request', group_id)

    #who triggered this action?
    notification.add_actor(current_user.get_id())

    #who to notify?
    notification.add_notifier(user_id)

    membership = Membership.query.filter(Membership.group_id == group_id, Membership.user_id == user_id).first()
    membership.status = 1
    db.session.commit()
    return redirect(url_for("admin.group_requests", id=group_id))

@admin.route('/decline_request/<string:group_id>/<string:user_id>')
@admin_required
def decline_request(group_id, user_id):
    membership = Membership.query.filter(Membership.group_id == group_id, Membership.user_id == user_id).first()
    membership.status = 3
    db.session.commit()
    return redirect(url_for("admin.group_requests", id=group_id))