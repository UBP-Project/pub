from flask import render_template, flash, redirect, url_for
from . import admin
from .forms import CreateUserForm, CreateInterestGroupForm, CreateActivity
from app import db
from ..models import User, Interest_Group, Activity, Membership

@admin.route('/', methods=['GET'])
def index():
    return render_template('admin_index.html');

@admin.route('/users/create', methods=['GET', 'POST'])
def create_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        user = User(firstname=form.firstname.data, 
            email=form.email.data)
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash("Success creating user")
        return redirect(url_for("admin.index"))
    return render_template('user/create.html', form=form)


# group management
@admin.route('/groups')
def groups():
    groups = Interest_Group.query.all()
    return render_template('group/groups.html', groups=groups)

@admin.route('/groups/<int:id>', methods=['GET', 'POST'])
def view_group(id):
    group = Interest_Group.query.get_or_404(id)
    members = User.query \
        .join(Membership, User.id==Membership.user_id) \
        .filter(Membership.group_id==id, Membership.status != 0)
    return render_template('group/view_group.html', group=group, members=members)

@admin.route('/groups/create', methods=['GET', 'POST'])
def create_interest_group():
    print('point 1')
    form = CreateInterestGroupForm()
    print('point 2')
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
    return render_template('group/create.html', form=form)


# activity management
@admin.route('/activities/<int:id>')
def view_activity(id):
    activity = Activity.query.filter_by(id=id).first()
    if activity is not None:
        return render_template("activity/view_activity.html", activity=activity)
    return redirect(url_for("admin.index"))

@admin.route('/activities/create', methods=['GET', 'POST'])
def create_activity():
    form = CreateActivity()
    if form.validate_on_submit():
        activity = Activity(
            title = form.title.data,
            description = form.title.data,
            start_date = form.start_date.data,
            end_date = form.start_date.data,
            address = form.address.data)
        print(activity)
        db.session.add(activity)
        db.session.commit()
        flash("Success Creating Activity")
        return redirect(url_for("admin.index"))
    return render_template('activity/create.html', form=form)



