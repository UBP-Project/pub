from flask import render_template, flash, redirect, url_for
from .. import admin
from ...forms import CreateUserForm
from app import db
from ...models import User

@admin.route('/users')
def users():
    users = User.query.all()
    return render_template('user/users.html', users=users)

@admin.route('/users/<int:id>')
def profile(id):
    user = User.query.get_or_404(id)
    return render_template('user/profile.html', user=user)

@admin.route('/users/create', methods=['GET', 'POST'])
def create_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        user = User(firstname=form.firstname.data,
            middlename=form.middlename.data,
            lastname=form.lastname.data, 
            email=form.email.data,
            department=form.department.data,
            position=form.position.data,
            birthday=form.birthday.data)
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash("Success creating user")
        return redirect(url_for("admin.index"))
    return render_template('user/create.html', form=form)