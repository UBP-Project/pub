from flask import render_template, flash, redirect, url_for
from .. import admin
from ...forms import CreateInterestGroupForm
from app import db
from ...models import User, Interest_Group, Membership

@admin.route('/groups')
def groups():
    groups = Interest_Group.query.all()
    return render_template('admin/group/groups.html', groups=groups)

@admin.route('/groups/<int:id>', methods=['GET', 'POST'])
def group(id):
    group = Interest_Group.query.get_or_404(id)
    members = User.query \
        .join(Membership, User.id==Membership.user_id) \
        .filter(Membership.group_id==id, Membership.status != 0)
    return render_template('admin/group/group.html', group=group, members=members)

@admin.route('/groups/create', methods=['GET', 'POST'])
def create_group():
    form = CreateInterestGroupForm()
    if form.validate_on_submit():
        interest_group = Interest_Group(
            name=form.name.data,
            about=form.about.data,
            cover_photo=form.cover_photo.data,
            group_icon=form.group_icon.data)
        db.session.add(interest_group)
        db.session.commit()
        flash("Success creating group")
        return redirect(url_for("admin.index"))
    return render_template('admin/group/create.html', form=form)