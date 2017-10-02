from flask import render_template, redirect, url_for, request
from .. import admin
from ...forms import CreateActivityForm, UpdateActivityForm
from app import db
from app.models import Activity, Interest_Group
from ...decorators import admin_required
from ...utils import flash_errors, is_valid_extension
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
from sqlalchemy import or_
from PIL import Image

ACTIVITIES_PER_PAGE = 16

IMAGE_SIZES = [
    (600, 250), #modal cover photo
    (260, 200)  #card
]

@admin.route('/activities/<uuid(strict=False):id>')
@admin_required
def activity(id):
    activity = Activity.query.get_or_404(id)
    return render_template("admin/activity/view_activity.html",
                           activity=activity)


@admin.route('/activities/create', methods=['GET', 'POST'])
@admin_required
def create_activity():
    form = CreateActivityForm()
    groups = Interest_Group.query.all()
    if request.method == 'POST':
        image = form.image.data
        image_filename = secure_filename(image.filename)
        extension = image_filename.rsplit('.', 1)[1].lower()
        image_hashed_filename = str(uuid.uuid4().hex) + '.' + extension
        
        file_path = os.path.join('app/static/uploads/activity_images', image_hashed_filename)

        image.save(file_path)

        image = Image.open(file_path)

        #resize image
        for size in IMAGE_SIZES:
            new_image = image.resize(size)

            directory = 'app/static/uploads/activity_images/' + str(size[0]) + 'x'+ str(size[1]) + '/'

            if not os.path.isdir(directory):
                os.makedirs(directory)

            new_image.save(os.path.join(directory, image_hashed_filename))
            
        # create the activity
        activity = Activity(
            title=form.title.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.start_date.data,
            address=form.address.data,
            group_id=None if form.group.data == "None" else uuid.UUID(
                form.group.data).hex,
            image=image_hashed_filename)
        db.session.add(activity)
        db.session.commit()
        db.session.refresh(activity)

        # set activity point on: interested, going, attended
        activity.set_points('going', form.going_point.data)
        activity.set_points('interested', form.interested_point.data)
        activity.set_points('attended', form.attended_point.data)

        # after creating the activity return to list of activities
        return redirect(url_for("admin.activities"))
    return render_template('admin/activity/create.html',
                           form=form, groups=groups)


@admin.route('/activities')
@admin_required
def activities():

    query = None
    start_date = None
    end_date = None
    if request.args.get('query') is not None:
        query = request.args.get('query')
        q = query.lower()

    start_date_str = request.args.get('start_date')
    if start_date_str is not None and len(start_date_str) > 0:
        start_date = datetime.strptime(start_date_str, '%a %b %d %Y')

    end_date_str = request.args.get('end_date')
    if end_date_str is not None and len(end_date_str) > 0:
        end_date = datetime.strptime(end_date_str, '%a %b %d %Y')

    if request.args.get('page') is not None:
        page = int(request.args.get('page'))
    else:
        page = 1

    # filters activities base on the
    #   parameters: query, start_date, and end_date
    if query is not None and start_date is not None and end_date is not None:
        activities = Activity.query.filter(
            or_(Activity.title.ilike("%" + q + "%"),
                Activity.description.ilike("%" + q + "%")),
            Activity.start_date >= start_date,
            Activity.end_date <= end_date)\
            .order_by(Activity.start_date)\
            .paginate(page=page, per_page=ACTIVITIES_PER_PAGE, error_out=False)
    elif query is not None and start_date is not None:
        activities = Activity.query.filter(
            or_(Activity.title.ilike("%" + q + "%"),
                Activity.description.ilike("%" + q + "%")),
            Activity.start_date >= start_date).order_by(Activity.start_date)\
            .paginate(page=page, per_page=ACTIVITIES_PER_PAGE, error_out=False)
    elif query is not None:
        activities = Activity.query.filter(
            or_(Activity.title.ilike("%" + q + "%"),
                Activity.description.ilike("%" + q + "%")))\
            .order_by(Activity.start_date)\
            .paginate(page=page, per_page=ACTIVITIES_PER_PAGE, error_out=False)
    elif start_date is not None and end_date is not None:
        activities = Activity.query.filter(
            Activity.start_date >= start_date,
            Activity.end_date <= end_date).order_by(Activity.start_date)\
            .paginate(page=page, per_page=ACTIVITIES_PER_PAGE, error_out=False)
    elif start_date is not None:
        activities = Activity.query.filter(
            Activity.start_date >= start_date).order_by(Activity.start_date)\
            .paginate(page=page, per_page=ACTIVITIES_PER_PAGE, error_out=False)
    elif end_date is not None:
        activities = Activity.query.filter(
            Activity.end_date <= end_date).order_by(Activity.start_date)\
            .paginate(page=page, per_page=ACTIVITIES_PER_PAGE, error_out=False)
    else:
        activities = Activity.query.order_by(Activity.start_date)\
            .paginate(page=page, per_page=ACTIVITIES_PER_PAGE, error_out=False)

    return render_template('admin/activity/activities.html',
                           activities=activities, query=query,
                           start_date=start_date_str, end_date=end_date_str)


@admin.route('/activities/<string:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_activity(id):
    form = UpdateActivityForm()
    activity = Activity.query.get_or_404(id)

    if request.method == 'POST' and request.form.get('delete') == 'delete':
        db.session.delete(activity)
        return redirect(url_for('admin.activities'))

    if request.method == 'POST':
        if form.image.data is not None:
            image = form.image.data
            image_filename = secure_filename(image.filename)
            if is_valid_extension(image_filename):
                extension = image_filename.rsplit('.', 1)[1].lower()
                image_hashed_filename = str(uuid.uuid4().hex) + '.' + extension
                file_path = os.path.join('app/static/uploads/activity_images',
                                         image_hashed_filename)
                image.save(file_path)
                activity.image = image_hashed_filename
        activity.title = form.title.data
        activity.description = form.description.data
        activity.start_date = form.start_date.data
        activity.end_date = form.end_date.data
        activity.address = form.address.data
        activity.group_id = None \
            if form.group.data == "None" \
            else uuid.UUID(form.group.data).hex
        db.session.commit()

        # edit points per activity action
        activity.edit_points('going', form.going_point.data)
        activity.edit_points('interested', form.interested_point.data)
        activity.edit_points('attended', form.attended_point.data)

        return redirect(url_for('admin.activities'))

    # load activity data to the form
    form.title.data = activity.title
    form.description.data = activity.description
    form.start_date.data = activity.start_date
    form.end_date.data = activity.end_date
    form.address.data = activity.address
    form.group.data = activity.group_id
    form.going_point.data = activity.get_points('going')
    form.interested_point.data = activity.get_points('interested')
    form.attended_point.data = activity.get_points('attended')
    flash_errors(form)
    return render_template('admin/activity/edit.html',
                           form=form, activity=activity)


@admin.route('/activities/<string:id>/attendance')
@admin_required
def attendance(id):
    activity = Activity.query.get_or_404(id)
    return render_template('admin/activity/attendance.html', activity=activity)
