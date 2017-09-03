from flask import url_for
from app import db
from app.models import User, Follow
from sqlalchemy_utils import UUIDType
from datetime import datetime
import uuid

class Notification(db.Model):
    __tablename__ = 'notification'
    id          = db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    # actor       = db.Column(UUIDType(binary=False))
    # notifier    = db.Column(UUIDType(binary=False))
    # entity      = db.Column(UUIDType(binary=False), db.ForeignKey('notification_entity.id', onupdate='CASCADE', ondelete='CASCADE'))
    # content     = db.Column(db.Text(4294967295))
    # timestamp   = db.Column(db.Date)
    # url         = db.Column(db.String(50))
    # is_read     = db.Column(db.Boolean)
    notification_object_id = db.Column(UUIDType(binary=False), db.ForeignKey('notification_object.id'))
    notifier_id = db.Column(UUIDType(binary=False), db.ForeignKey('user.id'))
    status = db.Column(db.Boolean)


    # def __init__(self, user_id, content, url):
    #     self.user_id    = user_id
    #     self.content    = content
    #     self.timestamp  = datetime.utcnow()
    #     self.url        = url
    #     self.is_read    = False
    def __init__(self, notification_object_id, notifier_id):
        self.notification_object_id = notification_object_id
        self.notifier_id = notifier_id
        self.status = False

    def __repr__(self):
        return '<Notification %r>' % self.id

    # def to_json(self):
    #     json = {
    #         'id'        : self.id,
    #         'content'   : self.content,
    #         'timestamp' : self.timestamp,
    #         'url'       : self.url,
    #         'is_read'   : self.is_read 
    #     }

    #     return json

    # def from_json(json_notification):
    #     user_id     = json_notification.get('user_id')
    #     content     = json_notification.get('content')
    #     timestamp   = json_notification.get('timestamp')
    #     url         = json_notification.get('url')
    #     return Notification(user_id=user_id, content=content, url=url)
