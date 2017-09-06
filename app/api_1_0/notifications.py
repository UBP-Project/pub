from flask import jsonify, request, current_app, url_for
from flask_login import login_required, current_user

from sqlalchemy import exc

from app.models import User, Follow, Notification, Notification_Object, Notification_Change, Notification_EntityType
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
      - name: page
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
    if 'page' in request.args:
        page = int(request.args.get('page'))
    else:
        page = 1

    notifications = Notification.query\
        .add_columns(Notification.id, Notification.status, Notification.timestamp, Notification.notification_object_id)\
        .join(Notification_Object)\
        .join(Notification_EntityType)\
        .filter(Notification.notifier_id == current_user.get_id())\
        .add_columns(Notification_EntityType.action, Notification_EntityType.entity)\
        .order_by(Notification.timestamp.desc())\
        .distinct()\
        .paginate(page = page, per_page = 10, error_out = False).items

    return jsonify([
            {
                'object_id' : notification.notification_object_id,
                'id'        : notification.id,
                'status'    : notification.status,
                'timestamp' : notification.timestamp,
                'action'    : notification.action,
                'entity'    : notification.entity,
                'actors'    : [
                    {
                        'id'           : actor.id,
                        'firstname'    : actor.firstname,
                        'middlename'   : actor.middlename,
                        'lastname'     : actor.lastname,
                        'email'        : actor.email,
                        'department'   : actor.department,
                        'position'     : actor.position,
                        'birthday'     : actor.birthday
                    } for actor in User.query.join(Notification_Change).join(Notification_Object, Notification_Object.id == notification.notification_object_id).all()
                ]
            }
            for notification in notifications
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

    if notification.status is False:
        notification.status = True

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

    if notification.status is True:
        notification.status = False

    try:
        db.session.commit()
        return  jsonify({'status': 'Success'}), 200# change this to better message format
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500