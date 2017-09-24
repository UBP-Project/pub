from flask import jsonify, request, current_app, url_for
from flask_login import login_required, current_user

from sqlalchemy import exc

from app.models import User, Follow, Notification, Notification_Object, Notification_EntityType
from app.api_1_0 import api
from app.notification import Notif
from app import db
import json

@api.route('/notifications', methods=['GET'])
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
        default: 1

    responses:
        200:
            description: OK
    """
    if 'page' in request.args:
        page = int(request.args.get('page'))
    else:
        page = 1

    notifications = Notification_EntityType.query\
                        .join(Notification_Object)\
                        .add_columns(Notification_EntityType.entity, Notification_EntityType.action)\
                        .add_columns(Notification_Object.id.label('object_id'), Notification_Object.timestamp.label('object_timestamp'), Notification_Object.entity_id.label('entity_id'))\
                        .join(Notification)\
                        .join(User, Notification.actor_id == User.id)\
                        .add_columns(Notification.actor_id)\
                        .join(Follow, User.id == Follow.follower_id)\
                        .filter(Notification_Object.status == True)\
                        .order_by(Notification.timestamp.desc())\
                        .paginate(page=page, per_page=10, error_out=False)

    return jsonify(
        {
            'has_next': notifications.has_next,
            'has_prev': notifications.has_prev,
            'notifications' : [{
                'object_id'         : notification.object_id,
                'object_timestamp'  : notification.object_timestamp,
                'entity_type'       : notification.entity,
                'entity'            : Notif.get_entity(notification.entity, notification.entity_id),
                'action'            : notification.action,
                'actor'             : User.query.get(notification.actor_id).to_json()
            } for notification in notifications.items]
        }
    ), 200