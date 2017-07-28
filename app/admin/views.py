from flask import render_template, flash
from . import admin
from .forms import CreateUserForm, CreateInterestGroupForm, CreateActivityForm
from app import db
from ..models import User, Interest_Group, Activity

@admin.route('/', methods=['GET'])
def index():
    return render_template('admin/index.html');

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
        return render_template('admin/index.html')
    return render_template('users/create.html', form=form)

@admin.route('/groups/create', methods=['GET', 'POST'])
def create_interest_group():
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
        return render_template('admin/index.html')
    return render_template('groups/create.html', form=form)

@admin.route('/activities/create', methods=['GET', 'POST'])
def create_activity():
    form = CreateActivityForm()
    if form.validate_on_submit():
        activity = Activity(
            title = form.title.data,
            description = form.title.data,
            start_date = form.start_date.data,
            end_date = form.start_date.data,
            address = form.address.data,
            group_id=form.address.data)
        db.session.add(activity)
        db.session.commit()
        flash("Success Creating Activity")
        return render_template('admin/index.html')
    return render_template('activities/create.html', form=form)



