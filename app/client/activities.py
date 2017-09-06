from flask import render_template, flash, redirect, url_for, request
from .. import admin
from ..forms import CreateActivityForm, UpdateActivityForm
from app import db
from app.models import User, Activity, Permission, Interest_Group
from ..utils import flash_errors, is_valid_extension
from werkzeug.utils import secure_filename
import os
import uuid
from . import client
from flask_login import current_user, login_required
from ..auth import is_manager_or_leader

@client.route('/activities/')
@login_required
def activities():
    show_create = is_manager_or_leader()
    activities = Activity.query.limit(7)
    return render_template("client/views/activities.html", activities=activities,\
        show_create=show_create, user=current_user)

@client.route('/activities/<string:id>')
@login_required
def activity(id):
    activity = Activity.query.get_or_404(id)
    return render_template('client/activity/activity.html', activity=activity)

@client.route('/activities/create', methods=['GET', 'POST'])
@login_required
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
        return redirect(url_for("client.activity", id=activity.id))
    flash_errors(form)
    return render_template("client/activity/create.html", form=form, groups=groups)

# @client.route('/activities/<string:id>/attendance')
# @login_required
# @manager_or_leader_only
# def attendance(id):
    