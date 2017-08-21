from flask import jsonify, request, current_app, url_for
from flask_login import login_required, current_user

from sqlalchemy import exc

from app.models import User, Follow, Notification
from app.api_1_0 import api
# from app.api_1_0.decorators import follow_notif

# from app import db
import json

@api.route('/notification')
@login_required
def get_notifications():
	"""
    Get Notifications
    ---
    tags:
      - notifications

    parameters:
      - name: limit
        in: query
        example: 1
        default: 10

    responses:
        200:
            description: OK
            schema:
                id: notifications
                properties:
                    id:
                        type: string
                        example: 0f5b5ff8-afa2-43f7-8066-8ec3075c4c0c
                        required: true

                    user_id:
                        type: string
                        example: 0f5b5ff8-afa2-43f7-8066-8ec3075c4c0c
                        required: true

                    content:
                        type: string
                        example: Some text here
                        required: true

                    timestamp:
                        type: string
                        format: date
                        example: 2017-08-20
                        required: true

                    url:
                        type: string
                        example: http://....
                        required: true

                    is_read:
                        type: boolean
                        description: Hashed password
                        required: true
    """
    try:
    	if 'limit' in request.args:
    		limit = request.args.get('limit')
    		notifications = Notification.query.filter(user_id=current_user.get_id()).limit(limit)
    	else:
    		notifications = Notification.query.filter(user_id=current_user.get_id()).all()
    except exc.SQLAochemyError as e:
        print(e)

	return jsonify([
		notification.to_json() for notification in notifications
	]), 200