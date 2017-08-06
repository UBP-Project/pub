from flask import render_template, flash, redirect, url_for
from .. import admin
from ...forms import CreateActivity
from app import db
from ...models import User, Activity, Permission
from ...decorators import admin_required, permission_required

@admin.route('/activities/<int:id>')
def view_activity(id):
    activity = Activity.query.get_or_404(id)
    if activity is not None:
        return render_template("admin/activity/view_activity.html", activity=activity)
    return redirect(url_for("admin.index"))

@admin.route('/activities/create', methods=['GET', 'POST'])
# @permission_required(Permission.CREATE_ACTIVITY)
def create_activity():
    form = CreateActivity()
    if form.validate_on_submit():
        activity = Activity(
            title = form.title.data,
            description = form.description.data,
            start_date = form.start_date.data,
            end_date = form.start_date.data,
            address = form.address.data)
        print(activity)
        db.session.add(activity)
        db.session.commit()
        flash("Success Creating Activity")
        return redirect(url_for("admin.index"))
    return render_template('admin/activity/create.html', form=form)

@admin.route('/activities')
def activities():
    return "Activities";