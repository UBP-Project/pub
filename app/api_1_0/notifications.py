from flask import jsonify, request
from app.models import User, Follow, Notification, Notification_Object, Entity
from app.api_1_0 import api
from app.notification import Notif
from flask_login import current_user


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

    notifications = Entity.query\
        .join(Notification_Object)\
        .join(Notification)\
        .join(User)\
        .join(Follow, User.id == Follow.following_id)\
        .add_columns(Entity.entity, Entity.action)\
        .add_columns(Notification_Object.id.label('object_id'),
            Notification_Object.timestamp.label('object_timestamp'),
            Notification_Object.entity_id)\
        .add_columns(Notification.actor_id)\
        .filter(Notification_Object.status == True,
            Follow.follower_id == current_user.get_id())\
        .order_by(Notification.timestamp.desc())\
        .paginate(page=page, per_page=10, error_out=False)

    return jsonify(
        {
            'has_next': notifications.has_next,
            'has_prev': notifications.has_prev,
            'notifications': [{
                'object_id': notification.object_id,
                'object_timestamp': notification.object_timestamp,
                'entity_type': notification.entity,
                'entity': Notif.get_entity(notification.entity, notification.entity_id),
                'action': notification.action,
                'actor': User.query.get(notification.actor_id).to_json()
            } for notification in notifications.items]
        }
    ), 200
