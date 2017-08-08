from flask import render_template, flash, redirect, url_for
from .. import admin
from ...forms import CreateActivityForm, UpdateActivityForm
from app import db
from ...models import User, Activity, Permission, Interest_Group
from ...decorators import admin_required, permission_required


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))

@admin.route('/activities/<int:id>')
@admin_required
def view_activity(id):
    activity = Activity.query.get_or_404(id)
    if activity is not None:
        return render_template("admin/activity/view_activity.html", activity=activity)
    return redirect(url_for("admin.index"))

@admin.route('/activities/create', methods=['GET', 'POST'])
@admin_required
def create_activity():
    form = CreateActivityForm()
    groups = Interest_Group.query.all()
    if form.validate_on_submit():
        activity = Activity(
            title = form.title.data,
            description = form.description.data,
            start_date = form.start_date.data,
            end_date = form.start_date.data,
            address = form.address.data,
            group_id = form.group.data)
        print(activity)
        db.session.add(activity)
        db.session.commit()
        flash("Success Creating Activity")
        return redirect(url_for("admin.index"))
    flash_errors(form)
    return render_template('admin/activity/create.html', form=form, groups=groups)

@admin.route('/activities')
@admin_required
def activities():
    activities = Activity.query.all()
    return render_template('admin/activity/activities.html', activities=activities);

@admin.route('/activities/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_activity(id):
    form                  = UpdateActivityForm()
    activity              = Activity.query.get_or_404(id)
    if form.validate_on_submit():
        activity.title       = form.title.data      
        activity.description = form.description.data
        activity.start_date  = form.start_date.data 
        activity.end_date    = form.end_date.data   
        activity.address     = form.address.data    
        activity.group_id       = form.group.data
        db.session.commit()

    # load activity data to the form
    form.title.data       = activity.title
    form.description.data = activity.description
    form.start_date.data  = activity.start_date
    form.end_date.data    = activity.end_date
    form.address.data     = activity.address
    form.group.data       = activity.group_id
    return render_template('admin/activity/edit.html', form=form, activity=activity)