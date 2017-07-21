from flask import jsonify, request, current_app, url_for
from ..models import Activity
from .. import db
from . import api
import json

@api.route('/activity/')
def get_activities():
    activities = Activity.query.all()
    return jsonify({
        'activities': [activity.to_json() for activity in activities]
    })

@api.route('/activity/<int:id>/')
def get_activity(id):
    activity = activity.query.get_or_404(id)
    return jsonify(activity.to_json())

@api.route('/activity/', methods=['POST'])
def new_activity():
    data = request.form.to_dict()
    activity = Activity.from_json(data)
    db.session.add(activity)
    db.session.commit()
    return jsonify(activity.to_json()), 201, \
        {'Location': url_for('api.new_activity', id=activity.id, _external=True)}

@api.route('/activity/<int:id>', methods=['PUT'])
def edit_activity(id):
    activity = Activity.query.filter_by(id=id).update(request.form.to_dict())
    db.session.commit()
    return "Update Success" # change this to better message format

@api.route('/activity/<int:id>', methods=['DELETE'])
def delete_activity(id):
    activity = Activity.query.filter_by(id=id).delete()
    db.session.commit()
    return "Delete Success"