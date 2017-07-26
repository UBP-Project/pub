from flask import render_template, flash
from . import admin
from .forms import CreateUserForm, CreateInterestGroupForm
from app import db
from ..models import User, Interest_Group

@admin.route('/', methods=['GET'])
def index():
    return render_template('admin/index.html');

@admin.route('/create_user', methods=['GET', 'POST'])
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
    return render_template('admin/create_user.html', form=form)

@admin.route('/create_interest_group', methods=['GET', 'POST'])
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
    return render_template('admin/create_interest_group.html', form=form)


