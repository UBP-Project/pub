from flask import render_template, flash, redirect, url_for
from .. import admin
from ...forms import CreateUserForm, UpdateUserForm
from app import db
from ...models import User
from ...decorators import admin_required

@admin.route('/users')
@admin_required
def users():
    users = User.query.filter(User.role_id != 2).all()
    managers = User.query.filter(User.role_id == 2).all()
    return render_template('admin/user/users.html', users=users, managers=managers)

@admin.route('/users/<int:id>', methods=['GET', 'POST'])
@admin_required
def profile(id):
    form = UpdateUserForm()
    user = User.query.get_or_404(id)
    form.firstname.data  = user.firstname
    form.lastname.data   = user.lastname
    form.email.data      = user.email
    form.department.data = user.department
    form.position.data   = user.position
    form.birthday.data   = user.birthday
    form.role.data       = user.role_id
    form.submit.data     = "Save Changes"
    if form.validate_on_submit():
        print(form.role.data)
        user.firstname  = form.firstname.data,
        user.middlename = form.middlename.data,
        user.lastname   = form.lastname.data, 
        user.email      = form.email.data,
        user.department = form.department.data,
        user.position   = form.position.data,
        user.birthday   = form.birthday.data,
        user.role_id    = int(form.role.data)
        user.password   = form.password.data
        db.session.add(user)
        db.session.commit()
    return render_template('admin/user/profile.html', user=user, form=form)

@admin.route('/users/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        print(form.role.data)
        user = User(firstname=form.firstname.data,
            middlename=form.middlename.data,
            lastname=form.lastname.data, 
            email=form.email.data,
            department=form.department.data,
            position=form.position.data,
            birthday=form.birthday.data,
            role_id=int(form.role.data))
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash("Success creating user")
        return redirect(url_for("admin.index"))
    return render_template('admin/user/create.html', form=form)

@admin.route('/managers')
@admin_required
def managers():
    return "Managers";