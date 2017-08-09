from flask import render_template, flash, redirect, url_for, request
from .. import admin
from ...forms import CreateInterestGroupForm
from app import db
from ...models import User, Interest_Group, Membership, Activity
from ...decorators import admin_required
from ...utils import flash_errors
from werkzeug.utils import secure_filename
import os
import uuid

@admin.route('/groups')
@admin_required
def groups():
    groups = Interest_Group.query.all()
    return render_template('admin/group/groups.html', groups=groups)

@admin.route('/groups/<int:id>', methods=['GET', 'POST'])
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
        return redirect(url_for("admin.index"))
    return render_template('admin/group/create.html', form=form)

@admin.route('/groups/setleader/<int:group_id>/<int:user_id>')
@admin_required
def setleader(group_id, user_id):
    membership = Membership.query.filter(Membership.group_id == group_id, Membership.user_id == user_id).first()
    membership.level = 1
    db.session.commit()
    return redirect(url_for("admin.group", id=group_id))

@admin.route('/removeleader/<int:group_id>/<int:user_id>')
@admin_required
def removeleader(group_id, user_id):
    membership = Membership.query.filter(Membership.group_id == group_id, Membership.user_id == user_id).first()
    membership.level = 0
    db.session.commit()
    return redirect(url_for("admin.group", id=group_id))