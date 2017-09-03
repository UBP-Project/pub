import json
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from . import client
from app import db
from app.models import User, Interest_Group, Activity, Membership, Role, Follow
from ..auth import manager_or_leader_only
from ..utils import flash_errors

@client.route('/activities/')
@login_required
def activities():
    activities = Activity.query.limit(7)
    return render_template("client/views/activities.html", activities=activities, user=current_user)

# @client.route('/activities/<string:id>/attendance')
# @login_required
# @manager_or_leader_only
# def attendance(id):
    