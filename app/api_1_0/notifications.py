from flask import jsonify, request, current_app, url_for
from flask_login import login_required, current_user

from sqlalchemy import exc

from app.models import User, Follow, Notification
from app.api_1_0 import api
# from app.api_1_0.decorators import follow_notif

from app import db
import json

@api.route('/notifications', methods=['GET'])
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
	if 'limit' in request.args:
		limit = request.args.get('limit')
		notifications = Notification.query.filter(Notification.user_id==current_user.get_id()).limit(limit)
	else:
		notifications = Notification.query.filter(Notification.user_id==current_user.get_id()).all()

	return jsonify([
		notification.to_json() for notification in notifications
	]), 200

@api.route('/notifications/<uuid(strict=False):id>/mark_read', methods=['PUT'])
@login_required
def mark_read(id):
    """
    Mark as Read
    ---
    tags:
      - notifications

    parameters:
      - name: id
        in: path
        type: string

    responses:
        200:
            description: OK
        404:
            description: Not Found
        500:
            description: Internal Server Error
    """
    notification = Notification.query.get_or_404(id)

    if notification.is_read is False:
        notification.is_read = True

    try:
        db.session.commit()
        return  jsonify({'status': 'Success'}), 200# change this to better message format
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500

@api.route('/notifications/<uuid(strict=False):id>/mark_unread', methods=['PUT'])
@login_required
def mark_unread(id):
    """
    Mark as Unread
    ---
    tags:
      - notifications

    parameters:
      - name: id
        in: path
        type: string

    responses:
        200:
            description: OK
        404:
            description: Not Found
        500:
            description: Internal Server Error
    """
    notification = Notification.query.get_or_404(id)

    if notification.is_read is True:
        notification.is_read = False

    try:
        db.session.commit()
        return  jsonify({'status': 'Success'}), 200# change this to better message format
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500