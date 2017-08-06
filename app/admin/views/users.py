from flask import render_template, flash, redirect, url_for
from .. import admin
from ...forms import CreateUserForm
from app import db
from ...models import User
from ...decorators import admin_required

@admin.route('/users')
# @admin_required
def users():
    users = User.query.all()
    return render_template('admin/user/users.html', users=users)

@admin.route('/users/<int:id>')
# @admin_required
def profile(id):
    user = User.query.get_or_404(id)
    return render_template('admin/user/profile.html', user=user)

@admin.route('/users/create', methods=['GET', 'POST'])
# @admin_required
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
def managers():
    return "Managers";