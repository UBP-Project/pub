from flask import jsonify, request, current_app, url_for
from . import api

@api.route('/activities/')
def get_activities():
    return "Activities"

@api.route('/activity/<int:id>/')
def get_activity(id):
    return "Data for Activity ID %s" % id