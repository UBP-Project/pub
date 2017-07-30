from flask import jsonify, request, current_app, url_for
from app.models import Activity
from app.api_1_0 import api
from app import db
import json

@api.route('/activities')
def get_activities():
    """
    This is the language awesomeness API
    Call this api passing a language name and get back its features
    ---
    tags:
      - sample API Documentation
    parameters:
      - name: language
        in: path
        type: string
        required: true
        description: The language name
      - name: size
        in: query
        type: integer
        description: size of awesomeness
    responses:
      500:
        description: Error The language is not awesome!
      200:
        description: A language with its awesomeness
        schema:
          id: awesome
          properties:
            language:
              type: string
              description: The language name
              default: Lua
            features:
              type: array
              description: The awesomeness list
              items:
                type: string
              default: ["perfect", "simple", "lovely"]

    """
    activities = Activity.query.all()
    return jsonify([
        activity.to_json() for activity in activities
    ])

@api.route('/activities/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def activities(id):
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

@api.route('/activities', methods=['POST'])
def new_activity():
    data = request.form.to_dict()
    activity = Activity.from_json(data)
    db.session.add(activity)
    db.session.commit()
    return jsonify(activity.to_json()), 201, \
        {'Location': url_for('api.new_activity', id=activity.id, _external=True)}
