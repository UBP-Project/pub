from flask import jsonify, request, current_app, url_for
from app.models import Activity, User, User_Activity
from app.api_1_0 import api
from app import db
import json
from flask_login import login_required
from ..auth import manager_or_leader_only

@api.route('/activities', methods=['GET'])
@login_required
def get_activities():
    """
    Get list of Activities
    ---
    tags:
      - activities
    responses:
      200:
        description: OK
        schema:
          id: activities
          properties:
            id:
                type: integer
                example: 1
            description:
                type: string
                example: Pa zumba ni president :)
            start_date:
                type: string
                format: date 
            end_date:
                type: string
                format: date 
            address:
                type: string
                example: Luneta Park
            group_id:
                type: integer
                default: None
                descripton: In case event is associated with some group
    """

    if 'limit' in request.args:
        limit = request.args.get('limit')
        activities = Activity.query.limit(limit)
    else:
        activities = Activity.query.all()

    return jsonify([
        activity.to_json() for activity in activities
    ])

@api.route('/activities/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def activities(id):
    """
    Read, Update, and Delete
    ---
    tags:
        - activities

    responses:
        200:
            description: OK
        500:
            description: Internal Server Error
    """
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

@api.route('/activities/<int:id>/going', methods=['GET'])
@login_required
def get_going(id):
    going = User.query                      \
        .join(User_Activity)                \
        .join(Activity)                     \
        .filter(Activity.id == id)          \
        .filter(User_Activity.status == 1)  \
        .order_by(User.lastname)

    return jsonify([
        user.to_json() for user in going
    ])

@api.route('/activities/<int:id>/interested', methods=['GET'])
@login_required
def get_interested(id):
    interested = User.query                 \
        .join(User_Activity)                \
        .join(Activity)                     \
        .filter(Activity.id == id)          \
        .filter(User_Activity.status == 0)  \
        .order_by(User.lastname)

    return jsonify([
        user.to_json() for user in interested
    ])

@api.route('/activities', methods=['POST'])
@login_required
def new_activity():
    """
    Create Activity
    ---
    tags:
        - activities
    parameters:
      - in: body
        name: body
        description: JSON parameters.
        schema:
          properties:
            title:
              type: string
              description: Name of the Activity
              example: UHAC Manila
            description:
              type: string
              description: Description of Activity.
              example: Hackathon for Digital Innovation
            start_date:
              type: string
              format: date
              description: Starting When?
              example: 2017-07-31
            end_date:
              type: string
              format: date
              description: Ending When?
              example: 2017-08-01
            group_id:
              type: integer
              description: If an acitivity is associated with a group
              example: 1
    responses:
        200:
            description: Success!
        500:
            description: Internal Server Error
    """
    data = request.form.to_dict()
    manager_or_leader_only(data.group_id)
    activity = Activity.from_json(data)
    db.session.add(activity)
    db.session.commit()
    return jsonify(activity.to_json()), 201, \
        {'Location': url_for('api.new_activity', id=activity.id, _external=True)}