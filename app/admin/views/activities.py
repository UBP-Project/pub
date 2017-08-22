from flask import render_template, flash, redirect, url_for, request
from .. import admin
from ...forms import CreateActivityForm, UpdateActivityForm
from app import db
from app.models import User, Activity, Permission, Interest_Group
from ...decorators import admin_required, permission_required
from ...utils import flash_errors, is_valid_extension
from werkzeug.utils import secure_filename
import os
import uuid


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))

@admin.route('/activities/<uuid(strict=False):id>')
@admin_required
def activity(id):
    activity = Activity.query.get_or_404(id)
    if activity is not None:
        return render_template("admin/activity/view_activity.html", activity=activity)
    return redirect(url_for("admin.index"))

@admin.route('/activities/create', methods=['GET', 'POST'])
@admin_required
def create_activity():
    form = CreateActivityForm()
    groups = Interest_Group.query.all()
    if request.method == 'POST':
        image                 = form.image.data
        image_filename        = secure_filename(image.filename)
        extension             = image_filename.rsplit('.', 1)[1].lower()
        image_hashed_filename = str(uuid.uuid4().hex) + '.' + extension
        file_path             = os.path.join('app/static/uploads/activity_images', image_hashed_filename)
        image.save(file_path)
        activity = Activity(
            title = form.title.data,
            description = form.description.data,
            start_date = form.start_date.data,
            end_date = form.start_date.data,
            address = form.address.data,
            group_id = None if form.group.data == "None" else uuid.UUID(form.group.data).hex,
            image = image_hashed_filename)
        print(activity)
        db.session.add(activity)
        db.session.commit()
        # flash("Success Creating Activity")
        return redirect(url_for("admin.activities"))
    flash_errors(form)
    return render_template('admin/activity/create.html', form=form, groups=groups)

@admin.route('/activities')
@admin_required
def activities():
    activities = Activity.query.all()
    return render_template('admin/activity/activities.html', activities=activities);

@admin.route('/activities/<string:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_activity(id):
    form                  = UpdateActivityForm()
    activity              = Activity.query.get_or_404(id)

    if request.method == 'POST' and request.form.get('delete') == 'delete':
        db.session.delete(activity)
        return redirect(url_for('admin.activities'))

    if request.method == 'POST':
        if form.image.data is not None:
            image                 = form.image.data
            image_filename        = secure_filename(image.filename)
            if is_valid_extension(image_filename):
                extension             = image_filename.rsplit('.', 1)[1].lower()
                image_hashed_filename = str(uuid.uuid4().hex) + '.' + extension
                file_path             = os.path.join('app/static/uploads/activity_images', image_hashed_filename)
                image.save(file_path)
                activity.image   = image_hashed_filename
        activity.title       = form.title.data      
        activity.description = form.description.data
        activity.start_date  = form.start_date.data 
        activity.end_date    = form.end_date.data   
        activity.address     = form.address.data
        activity.group_id    = None if form.group.data == "None" else uuid.UUID(form.group.data).hex
        db.session.commit()
        return redirect(url_for('admin.activities'))

    # load activity data to the form
    form.title.data       = activity.title
    form.description.data = activity.description
    form.start_date.data  = activity.start_date
    form.end_date.data    = activity.end_date
    form.address.data     = activity.address
    form.group.data       = activity.group_id
    flash_errors(form)
    return render_template('admin/activity/edit.html', form=form, activity=activity)

@admin.route('/wysiwyg')
def wysiwyg():
    return render_template('admin/activity/wysiwyg.html')