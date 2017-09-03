from flask import render_template, flash, redirect, url_for, request
from .. import admin
from ...forms import CreateUserForm, UpdateUserForm, PasswordForm
from app import db
from app.models import User, Role
from ...decorators import admin_required
from ...utils import flash_errors
from sqlalchemy import or_
import uuid
from werkzeug.utils import secure_filename
import os
from ...utils import flash_errors, is_valid_extension

USERS_PER_PAGE = 10

@admin.route('/users')
@admin_required
def users():
    query = request.args.get('query')
   
    if request.args.get('page') is not None:
        page = int(request.args.get('page'))
    else:
        page = 1
        
    if query is not None:
        users = User.query\
        .join(Role, Role.id == User.role_id)\
        .filter(Role.name == 'User', or_(\
            User.firstname.like("%"+str(query)+"%)"), \
            User.middlename.like("%"+str(query)+"%"), \
            User.lastname.like("%"+str(query)+"%"), \
            User.email.like("%"+str(query)+"%"), \
            User.department.like("%"+str(query)+"%"), \
            User.position.like("%"+str(query)+"%") \
        )).paginate(page=page, per_page=USERS_PER_PAGE, error_out=False)
    else:
        users = User.query\
        .join(Role, Role.id == User.role_id)\
        .filter(Role.name == 'User').paginate(page=page, per_page=USERS_PER_PAGE, error_out=False)
        query = ""
    return render_template('admin/user/users.html', users=users, query=query)

@admin.route('/users/managers')
@admin_required
def managers():
    query = request.args.get('query')
    page = 1
    if request.args.get('page') is not None:
        page = int(request.args.get('page'))
        
    if query is not None:
        managers = User.query\
            .join(Role, Role.id == User.role_id)\
            .filter(Role.name == 'Manager', or_(\
                User.firstname.like("%"+str(query)+"%)"), \
                User.middlename.like("%"+str(query)+"%"), \
                User.lastname.like("%"+str(query)+"%"), \
                User.email.like("%"+str(query)+"%"), \
                User.department.like("%"+str(query)+"%"), \
                User.position.like("%"+str(query)+"%") \
            )).paginate(page=page, per_page=USERS_PER_PAGE, error_out=False)
    else:
        managers = User.query\
            .join(Role, Role.id == User.role_id)\
            .filter(Role.name == 'Manager').paginate(page=page, per_page=USERS_PER_PAGE, error_out=False)
        query = ""
    return render_template('admin/user/managers.html', managers=managers, query=query)


@admin.route('/users/<string:id>', methods=['GET', 'POST'])
@admin_required
def profile(id):
    form = UpdateUserForm()
    user = User.query.get_or_404(id)

    if request.method == 'POST' and request.form.get('delete') == 'delete':
        db.session.delete(user)
        return redirect(url_for('admin.users'))

    if request.method == 'POST':
        if form.image.data is not None:
            image                 = form.image.data
            image_filename        = secure_filename(image.filename)
            if is_valid_extension(image_filename):
                extension             = image_filename.rsplit('.', 1)[1].lower()
                image_hashed_filename = str(uuid.uuid4().hex) + '.' + extension
                file_path             = os.path.join('app/static/uploads/profile_pictures', image_hashed_filename)
                image.save(file_path)
                user.image   = image_hashed_filename
        user.firstname  = form.firstname.data,
        user.middlename = form.middlename.data,
        user.lastname   = form.lastname.data, 
        user.email      = form.email.data,
        user.department = form.department.data,
        user.position   = form.position.data,
        user.birthday   = form.birthday.data,
        user.role_id    = form.role.data

        db.session.commit()
        return redirect(url_for('admin.users'))

    # load the current user info to the form
    form.firstname.data  = user.firstname
    form.middlename.data = user.middlename
    form.lastname.data   = user.lastname
    form.email.data      = user.email
    form.department.data = user.department
    form.position.data   = user.position
    form.birthday.data   = user.birthday
    form.role.data       = str(user.role_id)
    return render_template('admin/user/profile.html', user=user, form=form)

@admin.route('/users/<string:id>/change-password', methods=['GET', 'POST'])
@admin_required
def change_password(id):
    form = PasswordForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        return redirect(url_for('admin.profile', id=id))
    return render_template('admin/user/change-password.html', user=user, form=form)


@admin.route('/users/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    form = CreateUserForm()
    if request.method == 'POST':
        image                 = form.image.data
        image_filename        = secure_filename(image.filename)
        extension             = image_filename.rsplit('.', 1)[1].lower()
        image_hashed_filename = str(uuid.uuid4().hex) + '.' + extension
        file_path             = os.path.join('app/static/uploads/profile_pictures', image_hashed_filename)
        image.save(file_path)
        user = User(
            firstname=form.firstname.data,
            middlename=form.middlename.data,
            lastname=form.lastname.data, 
            email=form.email.data,
            department=form.department.data,
            position=form.position.data,
            birthday=form.birthday.data,
            role_id=uuid.UUID(form.role.data).hex,
            image=image_hashed_filename)
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        # flash("Success creating user")
        return redirect(url_for("admin.users"))
    flash_errors(form)
    return render_template('admin/user/create.html', form=form)