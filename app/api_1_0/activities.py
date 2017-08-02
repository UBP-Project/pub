from flask import jsonify, request, current_app, url_for
from app.models import Activity
from app.api_1_0 import api
from app import db
import json

@api.route('/activities')
def get_activities():
    """
    Get all Activities
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
    activities = Activity.query.all()
    return jsonify([
        activity.to_json() for activity in activities
    ])

# @api.route('/activities/<int:id>', methods=['GET', 'PUT', 'DELETE'])
# def activities(id):
#     """
#     Read, Update, and Delete
#     ---
#     tags:
#         - activities

#     responses:
#         200:
#             description: OK
#         500:
#             description: Internal Server Error
#     """
#     if request.method == 'GET':
#         activity = Activity.query.get_or_404(id)
#         return jsonify(activity.to_json())

#     elif request.method == 'PUT':
#         activity = Activity.query.filter_by(id=id).update(request.form.to_dict())
#         db.session.commit()
#         return "Updated" # change this to better message format

#     else:
#         activity = Activity.query.filter_by(id=id).delete()
#         db.session.commit()
#         return "Deleted"

@api.route('/activities/<int:id>', methods=['DELETE'])
def activities(id):
    """
    Delete Activity by id
    ---
    tags:
        - activities
    parameters:
      - in: paramater
        name: id
        type: integer
        required: true
        description: activity reference
    responses:
        200:
            description: Success!
        404:
            description: Not Found!
        500:
            description: Internal Server Error
    """
    activity = Activity.query.filter_by(id=id).delete()
    db.session.commit()
    return "Deleted"

@api.route('/activities', methods=['POST'])
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
    activity = Activity.from_json(data)
    db.session.add(activity)
    db.session.commit()
    return jsonify(activity.to_json()), 201, \
        {'Location': url_for('api.new_activity', id=activity.id, _external=True)}
