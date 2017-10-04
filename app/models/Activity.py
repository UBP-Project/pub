from app import db
from app.models import Entity, Points_Type
from datetime import datetime
from sqlalchemy_utils import UUIDType
import uuid
from datetime import datetime
from flask_login import current_user
from werkzeug.utils import secure_filename
import os
from PIL import Image
from app.models import User, Role


class Activity(db.Model):

    __tablename__ = 'activity'
    id = db.Column(UUIDType(binary=False),
                   default=uuid.uuid4, primary_key=True)
    title = db.Column(db.String(200), unique=False)  # true on production
    description = db.Column(db.Text(4294967295))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String(100))
    group_id = db.Column(UUIDType(binary=False), db.ForeignKey(
        'interest_group.id', ondelete="CASCADE",
        onupdate="CASCADE"), nullable=True)
    image = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    creator_id = db.Column(UUIDType(binary=False), db.ForeignKey('user.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=True)

    def __init__(self, title, description, start_date, end_date, address, image, group_id=None):
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.address = address
        self.group_id = group_id
        self.image = image

        if current_user.is_authenticated:
            self.creator_id = current_user.get_id()
        else:
            admin = User.User.query.join(Role, Role.id == User.User.role_id)\
                .filter(Role.name == 'Administrator').first()
            self.creator_id = admin.id

    def __repr__(self):
        return '<Activity %r>' % self.title

    def to_json(self):
        json_post = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'address': self.address,
            'group_id': self.group_id,
            'image': self.image,
            'timestamp': self.timestamp
        }
        return json_post

    def set_points(self, action, value):
        entity = Entity.query.filter(
            Entity.entity == 'activity', Entity.action == action).first()
        points_type = Points_Type(entity.id, self.id, value)
        db.session.add(points_type)
        db.session.commit()

    def edit_points(self, action, value):
        points_type = Points_Type.query\
            .join(Entity, Entity.id == Points_Type.entity_type_id)\
            .filter(Points_Type.entity_id == self.id,
                    Entity.entity == 'activity',
                    Entity.action == action).first()
        if points_type is None:
            self.set_points(action, value)
        else:
            points_type.value = value
            db.session.commit()

    def get_points(self, action):
        points_type = Points_Type.query\
            .join(Entity, Entity.id == Points_Type.entity_type_id)\
            .filter(Points_Type.entity_id == self.id,
                    Entity.entity == 'activity',
                    Entity.action == action).first()
        if points_type is None:
            return 0
        return points_type.value

    def set_image(self, image):
        image_filename = secure_filename(image.filename)
        extension = image_filename.rsplit('.', 1)[1].lower()
        image_hashed_filename = str(uuid.uuid4().hex) + '.' + extension
        file_path = os.path.join(
            'app/static/uploads/activity_images', image_hashed_filename)
        image.save(file_path)

        image = Image.open(file_path)

        sizes = [
            (600, 250),  # modal cover photo
            (260, 200)  # card
        ]

        # resize image
        for size in sizes:
            new_image = image.resize(size)

            directory = 'app/static/uploads/activity_images/' + \
                str(size[0]) + 'x' + str(size[1]) + '/'

            if not os.path.isdir(directory):
                os.makedirs(directory)

            new_image.save(os.path.join(directory, image_hashed_filename))
        self.image = image_hashed_filename
        db.session.commit()

    @staticmethod
    def from_json(json_activity):
        title = json_activity.get('title')
        description = json_activity.get('description')
        start_date = json_activity.get('start_date')
        end_date = json_activity.get('end_date')
        address = json_activity.get('address')
        group_id = json_activity.get('group_id')
        image = json_activity.get('image')

        return Activity(title=title, description=description,
                        start_date=start_date, end_date=end_date,
                        address=address, group_id=group_id, image=image)
