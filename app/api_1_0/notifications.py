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

    # notifications = Notification.query\
    #     .add_columns(Notification.id, Notification.status, Notification.timestamp, Notification.notification_object_id)\
    #     .join(Notification_Object)\
    #     .add_columns(Notification_Object.entity_id)\
    #     .join(Notification_EntityType)\
    #     .filter(Notification_Object.status == True)\
    #     .filter(Notification.notifier_id == current_user.get_id())\
    #     .add_columns(Notification_EntityType.action, Notification_EntityType.entity)\
    #     .order_by(Notification.timestamp.desc())\
    #     .all()

    # return jsonify([
    #         {
    #             'notification_id'       : notification.id,
    #             'status'                : notification.status,
    #             'timestamp'             : notification.timestamp,
    #             'notification_object'   : notification.notification_object_id,
    #             'action'                : notification.action,
    #             'entity'                : notification.entity,
    #             'entity_object'         : Notif.get_entity(notification.entity, notification.entity_id),
    #             'actors'            : [
    #                 {
    #                     'id'           : actor.id,
    #                     'firstname'    : actor.firstname,
    #                     'middlename'   : actor.middlename,
    #                     'lastname'     : actor.lastname,
    #                     'email'        : actor.email,
    #                     'department'   : actor.department,
    #                     'position'     : actor.position,
    #                     'birthday'     : actor.birthday
    #                 } for actor in User.query.join(Notification_Change).join(Notification_Object).filter(Notification_Object.id == notification.notification_object_id).filter(Notification_Change.actor_id != current_user.get_id()).all()
    #             ]
    #         }
    #         for notification in notifications
    #     ]), 200
    
    # users = current_user.get_following()

    notifications = Notification_EntityType.query\
                        .add_columns(Notification_EntityType.entity, Notification_EntityType.action)\
                        .join(Notification_Object)\
                        .add_columns(Notification_Object.id.label('object_id'), Notification_Object.timestamp.label('object_timestamp'), Notification_Object.entity_id.label('entity_id'))\
                        .join(Notification)\
                        .join(User, Notification.actor_id == User.id)\
                        .add_columns(Notification.actor_id)\
                        .join(Follow, User.id == Follow.follower_id)\
                        .filter(Notification_Object.status == True)\
                        .order_by(Notification.timestamp.desc())\
                        .all()


    return jsonify([{
        'object_id'         : notification.object_id,
        'object_timestamp'  : notification.object_timestamp,
        'entity'            : Notif.get_entity(notification.entity, notification.entity_id),
        'action'            : notification.action,
        'actor'             : User.query.get(notification.actor_id).to_json()
    } for notification in notifications]), 200