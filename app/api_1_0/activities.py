from flask import jsonify, request, current_app, url_for
from sqlalchemy import exc
from app.models import Activity, User, User_Activity
from app.api_1_0 import api
from app import db
import json
from flask_login import login_required, current_user
from ..auth import manager_or_leader_only
from ..leaderboard import leaderboard

from app.utils import is_valid_extension
from werkzeug.utils import secure_filename
import os
import uuid

@api.route('/activities', methods=['GET'])
@login_required
def get_activities():
    """
    Get list of Activities
    ---
    tags:
      - activities

    parameters:
      - name: limit
        in: query
        example: 1
        default: 10

    responses:
      200:
        description: OK
        schema:
          id: activities
          properties:
            id:
                type: string
                example: 0f5b5ff8-afa2-43f7-8066-8ec3075c4c0c
            title:
                type: string
                example: Temple Run
                description: Event Title
            description:
                type: string
                example: Run Run Run
            start_date:
                type: string
                format: date 
                example: Sat, 19 Aug 2017 00:00:00 GMT
            end_date:
                type: string
                format: date 
                example: Sat, 19 Aug 2017 00:00:00 GMT
            address:
                type: string
                example: Luneta Park
            group_id:
                type: string
                default: None
                example: 0f5b5ff8-afa2-43f7-8066-8ec3075c4c0c
                descripton: In case event is associated with some group
            image:
                type: string
                example: 70a256f3628947508af68343821d78b6.jpg
                default: None
                description: File name of image in uploads/activity_image folder
    """

    if 'limit' in request.args:
        limit = request.args.get('limit')
        activities = Activity.query.limit(limit)
    else:
        activities = Activity.query.all()

    return jsonify([
        activity.to_json() for activity in activities
    ])

@api.route('/activities', methods=['POST'])
@login_required
def new_activity():
    """
    Create Activity
    ---
    tags:
        - activities
    parameters:
        - name: title
          in: formData
          type: string
          example: Temple Run
          description: Event Title
          default: Temple Run

        - name: description
          in: formData
          type: string
          example: Run Run Run
          description: Event Description
          default: Run Run Run

        - name: start_date
          in: formData
          type: string
          format: date
          example: '2017-08-19'
          description: Event Starting Date
          default: '2017-08-19'

        - name: end_date
          in: formData
          type: string
          format: date
          example: '2017-08-19'
          description: Event Ending date
          default: '2017-08-19'

        - name: address
          in: formData
          type: string
          exampe: Luneta Park
          description: Venue of the Event
          default: Luneta Park

        - name: group_id
          in: formData
          type: string
          example: 0f5b5ff8-afa2-43f7-8066-8ec3075c4c0c
          description: Event Association with groups
          default: 1

        - name: image
          in: formData
          type: file
          description: File name of image in uploads/activity_image folder

    responses:
        200:
            description: OK
        500:
            description: Internal Server Error
    """

    image                 = request.files.get('image')
    image_filename        = secure_filename(image.filename)

    if is_valid_extension(image_filename):
        extension             = image_filename.rsplit('.', 1)[1].lower()
        image_hashed_filename = str(uuid.uuid4().hex) + '.' + extension
        file_path             = os.path.join('app/static/uploads/activity_images', image_hashed_filename)
        image.save(file_path)
        activity = Activity(
            title       = request.form.get('title'),
            description = request.form.get('description'),
            start_date  = request.form.get('start_date'),
            end_date    = request.form.get('end_date'),
            address     = request.form.get('address'),
            group_id    = request.form.get('group_id'),
            image       = image_hashed_filename
        )
        db.session.add(activity)

    try:
        db.session.commit()
        return "Success" # change this to better message format
    except exc.SQLAlchemyError:
        db.session.rollback()
        return jsonify({'status':'error'}), 500

@api.route('/activities/<uuid(strict=False):id>', methods=['GET'])
@login_required
def get_activity_by(id):
    """
    Get an Activity by ID
    ---
    tags:
      - activities
    parameters:
        - name: id
          in: path
          type: string
          required: true
    responses:
      200:
        description: OK
        schema:
          id: activities
          properties:
            id:
                type: string
                example: 0f5b5ff8-afa2-43f7-8066-8ec3075c4c0c
            title:
                type: string
                example: Temple Run
                description: Event Title
            description:
                type: string
                example: Run Run Run
            start_date:
                type: string
                format: date 
                example: Sat, 19 Aug 2017 00:00:00 GMT
            end_date:
                type: string
                format: date 
                example: Sat, 19 Aug 2017 00:00:00 GMT
            address:
                type: string
                example: Luneta Park
            group_id:
                type: string
                default: None
                example: 0f5b5ff8-afa2-43f7-8066-8ec3075c4c0c
                descripton: In case event is associated with some group
            image:
                type: string
                example: 70a256f3628947508af68343821d78b6.jpg
                default: None
                description: File name of image in uploads/activity_image folder
    """
    activity = Activity.query.get_or_404(id)
    return jsonify(activity.to_json())

@api.route('/activities/<uuid(strict=False):id>', methods=['PUT'])
@login_required
def edit_activity_by(id):
    """
    Edit an Activity by ID
    ---
    tags:
      - activities

    parameters:

        - name: id
          in: path
          description: Event ID
          type: string
          required: true
          default: 04cb8787-fe54-4e73-80d4-c17bf56537ee

        - name: title
          in: formData
          type: string
          example: Temple Run
          description: Event Title
          default: Temple Run

        - name: description
          in: formData
          type: string
          example: Run Run Run
          description: Event Description
          default: Run Run Run

        - name: start_date
          in: formData
          type: string
          format: date
          example: '2017-08-19'
          description: Event Starting Date
          default: '2017-08-19'

        - name: end_date
          in: formData
          type: string
          format: date
          example: '2017-08-19'
          description: Event Ending date
          default: '2017-08-19'

        - name: address
          in: formData
          type: string
          exampe: Luneta Park
          description: Venue of the Event
          default: Luneta Park

        - name: group_id
          in: formData
          type: string
          example: 04cb8787-fe54-4e73-80d4-c17bf56537ee
          description: Event Association with groups
          default: 1

        - name: image
          in: formData
          type: file
          example: 70a256f3628947508af68343821d78b6.jpg
          description: File name of image in uploads/activity_image folder

    responses:
      200:
        description: OK
      500:
        description: Error
    """
    activity  = Activity.query.get_or_404(id)

    if 'image' in request.files:
        image                 = request.files.get('image')
        image_filename        = secure_filename(image.filename)
        if is_valid_extension(image_filename):
            extension             = image_filename.rsplit('.', 1)[1].lower()
            image_hashed_filename = str(uuid.uuid4().hex) + '.' + extension
            file_path             = os.path.join('app/static/uploads/activity_images', image_hashed_filename)
            image.save(file_path)
            activity.image   = image_hashed_filename
            
    activity.title       = request.form.get('title')      
    activity.description = request.form.get('description')
    activity.start_date  = request.form.get('start_date')
    activity.end_date    = request.form.get('end_date')   
    activity.address     = request.form.get('address')   
    activity.group_id    = request.form.get('group_id')

    try:
        db.session.commit()
        return "Success" # change this to better message format
    except exc.SQLAlchemyError:
        db.session.rollback()
        return jsonify({'status':'error'}), 500

@api.route('/activities/<uuid(strict=False):id>', methods=['DELETE'])
@login_required
def delete_activity_by(id):
    """
    Delete an Activity by ID
    ---
    tags:
      - activities

    parameters:
      - name: id
        in: path
        description: Event ID
        type: string
        required: true
        default: 04cb8787-fe54-4e73-80d4-c17bf56537ee

    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    activity = Activity.query.filter_by(id=id).delete()
    db.session.commit()
    return "Deleted"

@api.route('/activities/<uuid(strict=False):id>/going')
@login_required
def get_going_by(id):
    """
    Get list of Going individuals to an Activity
    ---
    tags:
      - activities

    parameters:
      - in: path
        name: id
        description: Group ID
    
    responses:
      200:
        description: OK
        schema:
          id: users
          properties:
            id:
                type: string
                example: 0f5b5ff8-afa2-43f7-8066-8ec3075c4c0c
                required: true

            firstname:
                type: string
                example: John
                required: true

            middlename:
                type: string
                example: Clinton
            
            lastname:
                type: string
                example: dela Cruz
                required: true

            email:
                type: string
                example: juandelacruz@gmail.com
                required: true

            password_hash:
                type: string
                example: pbkdf2:sha1:1000$bK0Jvvl7$974df4129556a5bdb11b7892b09275c6ed595f76             
                description: Hashed password
                required: true

            department:
                type: string
                example: Business Analytics
                description: Department where the employee belong
                required: true

            position:
                type: string
                example: Project Hire
                description: Job position
                required: true

            birthday:
                type: string
                format: date
                example: 1997-09-07

            role_id:
                type: string
                example: 0f5b5ff8-afa2-43f7-8066-8ec3075c4c0c
                description: Flag for user's role
                required: true
    """
    activity = Activity.query.get_or_404(id)

    going = User.query                      \
        .join(User_Activity)                \
        .join(Activity)                     \
        .filter(Activity.id == activity.id) \
        .filter(User_Activity.status == 1)  \
        .order_by(User.lastname)

    return jsonify([
        user.to_json() for user in going
    ])

@api.route('/activities/<uuid(strict=False):id>/interested')
@login_required
def get_interested(id):
    """
    Get list of Interested individuals to an Activity
    ---
    tags:
      - activities

    parameters:
      - in: path
        name: id
        description: Group ID
    
    responses:
      200:
        description: OK
        schema:
          id: users
          properties:
            id:
                type: string
                example: 04cb8787-fe54-4e73-80d4-c17bf56537ee

            firstname:
                type: string
                example: Juan
                description: First Name

            middlename:
                type: string
                example: y
                description: Middle Name

            lastname:
                type: string
                example: dela Cruz
                description: Last Name    
                
            email:
                type: string
                example: jdc@gmail.com
                description: User Email

            password_hash:
                type: string
                example: pbkdf2:sha1:1000$lnFVjrjG$b8cd6a98d9ab806eb52ca0066d275d59ee18e6f5
                description: User Password

            department:
                type: string
                example: Talen Acquisition
                description: UnionBank Dept

            position:
                type: string
                example: Head
                descripton: User's Position
            
            birthday:
                type: string
                format: date
                example: '1998-02-01'
                description: User Birthday

            role_id:
                type: string
                example: 04cb8787-fe54-4e73-80d4-c17bf56537ee
                description: Corresponding values for Administrator, Manager, and User
    """

    interested = User.query                 \
        .join(User_Activity)                \
        .join(Activity)                     \
        .filter(Activity.id == id)          \
        .filter(User_Activity.status == 0)  \
        .order_by(User.lastname)

    return jsonify([
        user.to_json() for user in interested
    ])

@api.route('/activities/<uuid(strict=False):id>/going', methods=['POST'])
@login_required
def going_to_activity_by(id):
    """
    Going to an Activity
    ---
    tags:
        - activities
    parameters:
        - name: id
          in: path
          type: string
          example: 04cb8787-fe54-4e73-80d4-c17bf56537ee
          description: Activity ID

    responses:
        200:
            description: Success
        409:
            description: Record already exists
        500:
            description: Internal Server Error
    """    
    activity = User_Activity.query.filter_by(user_id=current_user.get_id(), activity_id=id, status=1).first()

    if activity is not None:
        #check if the status is going
        return jsonify({'status': 'Record already exists'}), 201
    else:
      activity = User_Activity(
        user_id=current_user.get_id(),
        activity_id=id,
        status = 1 #going
        )
      db.session.add(activity)

      try:
          db.session.commit()
          leaderboard.joined_activity()
          return jsonify({'status': 'Success'}), 200        
      except exc.SQLAlchemyError as e:
          print(e)
          db.session().rollback()
          return jsonify({'status': 'error'}), 500

@api.route('/activities/<uuid(strict=False):id>/interested', methods=['POST'])
@login_required
def interested_to_activity_by(id):
    """
    Interested to an Activity
    ---
    tags:
        - activities
    parameters:
        - name: id
          in: path
          type: string
          example: 04cb8787-fe54-4e73-80d4-c17bf56537ee
          description: Activity ID

    responses:
        200:
            description: Success
        409:
            description: Record already exists
        500:
            description: Internal Server Error
    """    
    activity = User_Activity.query.filter_by(user_id=current_user.get_id(), activity_id=id, status=0).first()

    if activity is not None:
        #check if the status is going
        return jsonify({'status': 'Record already exists'}), 201
    else:
      activity = User_Activity(
        user_id=current_user.get_id(),
        activity_id=id,
        status = 0 #interested
        )
      db.session.add(activity)

      try:
          db.session.commit()
          return jsonify({'status': 'Success'}), 200
      except exc.SQLAlchemyError as e:
          db.session().rollback()
          return jsonify({'status': 'error'}), 500
