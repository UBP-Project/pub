from flask import jsonify, request, current_app, url_for
from app.models import Activity
from app.api_1_0 import api
from app import db
import json

@api.route('/activity')
def get_activities():
    activities = Activity.query.all()
    return jsonify([
        activity.to_json() for activity in activities
    ])

@api.route('/activity/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def activity(id):
    if request.method == 'GET':
        activity = Activity.query.get_or_404(id)
        return jsonify(activity.to_json())

    elif request.method == 'PUT':
        activity = Activity.query.filter_by(id=id).update(request.form.to_dict())
        db.session.commit()
        return "Updated" # change this to better message format

    else:
        activity = Activity.query.filter_by(id=id).delete()
        db.session.commit()
        return "Deleted"

@api.route('/activity', methods=['POST'])
def new_activity():
    data = request.form.to_dict()
    activity = Activity.from_json(data)
    db.session.add(activity)
    db.session.commit()
    return jsonify(activity.to_json()), 201, \
        {'Location': url_for('api.new_activity', id=activity.id, _external=True)}