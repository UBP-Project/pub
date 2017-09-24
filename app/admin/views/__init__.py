from flask import render_template, flash
from .. import admin
from ...decorators import admin_required
from . import activities, groups, users, perks, points
from app.models import Activity, User, Interest_Group
from datetime import datetime

@admin.route('/', methods=['GET'])
@admin_required
def index():
    upcoming_activities = Activity.query.filter(Activity.start_date >= datetime.now()).order_by(Activity.start_date).limit(4)
    new_users = User.query.order_by(User.timestamp.desc()).limit(6)
    new_groups = Interest_Group.query.order_by(Interest_Group.timestamp.desc()).limit(4)
    return render_template('admin/index.html',
        upcoming_activities=upcoming_activities,
        new_users=new_users,
        new_groups=new_groups);
