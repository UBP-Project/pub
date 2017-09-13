from flask import render_template, flash, redirect, url_for, request, jsonify
from .. import admin
from ..forms import CreateActivityFormClient, UpdateActivityFormClient
from app import db
from app.models import User, Activity, Permission, Interest_Group
from ..utils import flash_errors, is_valid_extension
from werkzeug.utils import secure_filename
import os
import uuid
from . import client
from flask_login import current_user, login_required
from ..auth import is_manager_or_leader, can_modify_activity

@client.route('/activities/')
@login_required
def activities():
    show_create = is_manager_or_leader()
    print(show_create)
    activities = Activity.query.limit(7)
    return render_template("client/activity/activities.html", activities=activities,\
        show_create=show_create, user=current_user)

@client.route('/myactivities/')
@login_required
def myactivities():
    show_create = is_manager_or_leader()
    activities = Activity.query.all()
    return render_template("client/activity/myactivities.html", activities=activities,\
        show_create=show_create, user=current_user)

@client.route('/activities/<string:id>')
@login_required
def activity(id):
    activity = Activity.query.get_or_404(id)
    return render_template('client/activity/activity.html', activity=activity)

@client.route('/activities/create', methods=['GET', 'POST'])
@login_required
def create_activity():
    is_manager_or_leader(abort_on_false=True) # Forbidden if not a leader or manager
    form = CreateActivityFormClient()
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
        return redirect(url_for("client.activity", id=activity.id))
    flash_errors(form)
    return render_template("client/activity/create.html", form=form, groups=groups)

@client.route('/activities/<string:id>/edit', methods=['GET', 'POST'])
def edit_activity(id):
    can_modify_activity(id, abort_on_false=True)
    form                  = UpdateActivityFormClient()
    activity              = Activity.query.get_or_404(id)
    if request.method == 'POST' and request.form.get('delete') == 'delete':
        db.session.delete(activity)
        return redirect(url_for('client.activities'))

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
        return redirect(url_for('client.activity', id=id))
    # load activity data to the form
    form.title.data       = activity.title
    form.description.data = activity.description
    form.start_date.data  = activity.start_date
    form.end_date.data    = activity.end_date
    form.address.data     = activity.address
    form.group.data       = activity.group_id
    flash_errors(form)
    return render_template('client/activity/edit.html', form=form, activity=activity)

@client.route('/activities/<string:id>/attendance')
@login_required
def attendance(id):
    is_manager_or_leader(abort_on_false=True) # Forbidden if not a leader or manager
    activity = Activity.query.get_or_404(id)
    return render_template("attendance/checklist.html", activity=activity)

@client.route('/activity-list')
@login_required
def activity_list():
    activities = Activity.query.all()
    return jsonify({
        'activities': [activity.to_json() for activity in activities]
    })
    