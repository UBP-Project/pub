from flask import render_template, flash, redirect, url_for, request, jsonify
from .. import admin
from ..forms import CreateActivityFormClient, UpdateActivityForm, UpdateActivityFormClient, CreateActivityForm
from app import db
from app.models import User, Activity, Permission, Interest_Group, Role, User_Activity
from ..utils import flash_errors, is_valid_extension
from werkzeug.utils import secure_filename
import os
import uuid
from . import client
from flask_login import current_user, login_required
from ..auth import is_manager_or_leader, can_modify_activity, is_manager
from PIL import Image

@client.route('/activities/')
@login_required
def activities():
    return render_template("client/activity/activities.html",
        can_manage_activity = is_manager_or_leader(), is_manager = is_manager(), user=current_user)

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
    if activity.creator_id is not None:
        creator = User.query.filter(User.id == activity.creator_id).first()
    else:
        creator = User.query.join(Role, Role.id == User.role_id)\
            .filter(Role.name == 'Administrator').first()
    going_users = User.query.join(User_Activity, User.id == User_Activity.user_id)\
        .filter(User_Activity.activity_id == id, User_Activity.status == 1).all()
    interested_users = User.query.join(User_Activity, User.id == User_Activity.user_id)\
        .filter(User_Activity.activity_id == id, User_Activity.status == 0).all()
    return render_template('client/activity/activity.html', activity=activity,
        going_users=going_users, interested_users=interested_users,
        can_edit_activity=can_modify_activity(id), creator=creator)

@client.route('/activities/create', methods=['GET', 'POST'])
@login_required
def create_activity():
    is_manager_or_leader(abort_on_false=True) # Forbidden if not a leader or manager

    if is_manager():
        form = CreateActivityForm() # all the groups 
    else:
        form = CreateActivityFormClient() # limited only to groups led

    groups = Interest_Group.query.all()
    if request.method == 'POST':
        activity = Activity(
            title = form.title.data,
            description = form.description.data,
            start_date = form.start_date.data,
            end_date = form.start_date.data,
            address = form.address.data,
            group_id = None if form.group.data == "None" else uuid.UUID(form.group.data).hex,
            image ='placeholder-activity.jpg')

        db.session.add(activity)
        db.session.commit()

        activity.set_image(form.image.data)

        # set activity point on: interested, going, attended
        activity.set_points('going', form.going_point.data)
        activity.set_points('interested', form.interested_point.data)
        activity.set_points('attended', form.attended_point.data)

        return redirect(url_for("client.activity", id=activity.id))
    flash_errors(form)
    return render_template("client/activity/create.html", form=form, groups=groups)

@client.route('/activities/<string:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_activity(id):
    can_modify_activity(id, abort_on_false=True)

    if is_manager():
        form = UpdateActivityForm() # all the groups 
    else:
        form = UpdateActivityFormClient() # limited only to groups led

    activity              = Activity.query.get_or_404(id)
    if request.method == 'POST' and request.form.get('delete') == 'delete':
        db.session.delete(activity)
        return redirect(url_for('client.activities'))

    if request.method == 'POST':
        if form.image.data is not None:
            activity.set_image(form.image.data)
        activity.title       = form.title.data      
        activity.description = form.description.data
        activity.start_date  = form.start_date.data 
        activity.end_date    = form.end_date.data   
        activity.address     = form.address.data
        activity.group_id    = None if form.group.data == "None" else uuid.UUID(form.group.data).hex
        db.session.commit()

        # edit points per activity action
        activity.edit_points('going', form.going_point.data)
        activity.edit_points('interested', form.interested_point.data)
        activity.edit_points('attended', form.attended_point.data)

        return redirect(url_for('client.activity', id=id))
    
    # load activity data to the form
    form.title.data            = activity.title
    form.description.data      = activity.description
    form.start_date.data       = activity.start_date
    form.end_date.data         = activity.end_date
    form.address.data          = activity.address
    form.group.data            = activity.group_id
    form.going_point.data      = activity.get_points('going')
    form.interested_point.data = activity.get_points('interested')
    form.attended_point.data   = activity.get_points('attended')
    flash_errors(form)
    return render_template('client/activity/edit.html', form=form, activity=activity)


@client.route('/activities/<string:id>/attendance')
@login_required
def attendance(id):
    is_manager_or_leader(abort_on_false=True)  # Forbidden if not a leader or manager
    activity = Activity.query.get_or_404(id)
    return render_template("attendance/checklist.html", activity=activity)

@client.route('/activities/<string:id>/summary')
@login_required
def summary(id):
    activity = Activity.query.get_or_404(id)
    return render_template("attendance/summary.html",
        can_manage_activity = can_modify_activity(id),
        is_manager = is_manager(), user=current_user, activity=activity)

@client.route('/activity-list')
@login_required
def activity_list():
    activities = Activity.query.all()
    return jsonify({
        'activities': [activity.to_json() for activity in activities]
    })
