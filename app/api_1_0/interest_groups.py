from flask import jsonify, request, url_for
from app import db
import json
from app.models import Interest_Group, Membership, User, Activity
from . import api
from flask_login import login_required, current_user
import datetime
from sqlalchemy import exc

from app.utils import is_valid_extension
from werkzeug.utils import secure_filename
import os
import uuid

@api.route('/interest_groups')
@login_required
def get_interest_groups():
    """
    Get list of Groups
    ---
    tags:
      - groups

    parameters:
      - name: limit
        in: query
        example: 1
        default: 15

    responses:
      200:
        description: OK
        schema:
          id: groups
          properties:
            id:
                type: integer
                example: 1

            name:
                type: string
                example: Sports
                description: Group name

            description:
                type: string
                example: Everything you should get involved!
                description: About the Group                

            cover_photo:
                type: string
                example: c94f84619ce845f3b6398a30aa99c720.bmp
                description: File name

            group_icon:
                type: string
                example: d167f8ec77194efc8319e3455da9920f.jpg
                description: File name
    """

    if 'limit' in request.args:
        limit = request.args.get('limit')
        interest_groups = Interest_Group.query.limit(limit)
    else:
        interest_groups = Interest_Group.query.all()
    
    return jsonify([
        interest_group.to_json() for interest_group in interest_groups
    ]), 200

@api.route('/interest_groups/<int:id>')
@login_required
def get_interest_group_by(id):
    """
    Get a Group by ID
    ---
    tags:
      - groups

    parameters:
      - name: id
        in: path
        example: 1
        required: true

    responses:
      200:
        description: OK
        schema:
          id: groups
          properties:
            id:
                type: integer
                example: 1
                required: true

            name:
                type: string
                example: Sports
                description: Group name
                required: true

            description:
                type: string
                example: Everything you should get involved!
                description: About the Group                

            cover_photo:
                type: string
                example: c94f84619ce845f3b6398a30aa99c720.bmp
                description: File name

            group_icon:
                type: string
                example: d167f8ec77194efc8319e3455da9920f.jpg
                description: File name
    """
    interest_group = Interest_Group.query.get_or_404(id)
    return jsonify(interest_group.to_json()), 200

@api.route('/interest_groups', methods=['POST'])
@login_required
def new_interest_group():
    """
    Create a Group
    ---
    tags:
      - groups

    parameters:
      - name: name
        in: formData
        example: Sports
        required: true
    
      - name: about
        in: formData
        example: Everything you should get involved!
        required: true
        
      - name: cover_photo
        in: formData
        type: file
        required: true

      - name: group_icon
        in: formData
        type: file
        required: true

    responses:
      200:
        description: Success
      409:
        description: Name already Taken
    
    """

     # handle upload group cover
    cover                 = request.files.get('cover_photo')
    cover_filename        = secure_filename(cover.filename)
    extension             = cover_filename.rsplit('.', 1)[1].lower()
    cover_hashed_filename = str(uuid.uuid4().hex) + '.' + extension
    file_path             = os.path.join('app/static/uploads/covers', cover_hashed_filename)
    cover.save(file_path)

    # handle upload user icon
    icon                 = request.files.get('group_icon')
    icon_filename        = secure_filename(icon.filename)
    extension            = icon_filename.rsplit('.', 1)[1].lower()
    icon_hashed_filename = str(uuid.uuid4().hex) + '.' + extension
    file_path            = os.path.join('app/static/uploads/group_icons', icon_hashed_filename)
    icon.save(file_path)

    interest_group = Interest_Group(
        name=request.request.form.get('name'),
        about=request.request.form.get('about'),
        cover_photo=cover_hashed_filename,
        group_icon=icon_hashed_filename)
    db.session.add(interest_group)

    try:
        db.session.commit()
        return jsonify(interest_group.to_json()), 200, \
            {'Location': url_for('api.new_interest_group', id=interest_group.id, _external=True)}
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': 'Name already taken'}), 409

@api.route('/interest_groups/<int:id>', methods=['PUT'])
@login_required
def edit_interest_group_by(id):
    """
    Edit an Interest Group by ID
    ---
    tags:
      - groups

    parameters:

        - name: id
          in: path
          description: Group ID
          type: integer
          required: true
          default: 1

        - name: name
          in: formData
          type: string
          example: Sports
          description: Group Name
          default: Sports

        - name: about
          in: formData
          type: string
          example: Everything you should get involved!
          description: Group Description
          default: Everything you should get involved!

        - name: cover_photo
          in: formData
          type: file
          required: true

        - name: group_icon
          in: formData
          type: file
          required: true

    responses:
      200:
        description: OK
      500:
        description: Error
    """
    group = Interest_Group.query.get_or_404(id)

    # handle upload group cover
    if 'cover_photo'in request.files:
        cover                 = request.files.get('cover_photo')
        cover_filename        = secure_filename(cover.filename)
        if is_valid_extension(cover_filename):
            extension             = cover_filename.rsplit('.', 1)[1].lower()
            cover_hashed_filename = str(uuid.uuid4().hex) + '.' + extension
            file_path             = os.path.join('app/static/uploads/covers', cover_hashed_filename)
            cover.save(file_path)
            group.cover_photo = cover_hashed_filename

    # handle upload user icon
    if 'group_icon' in request.files:
        icon                 = request.files.get('group_icon')
        icon_filename        = secure_filename(icon.filename)
        if is_valid_extension(icon_filename):
            extension            = icon_filename.rsplit('.', 1)[1].lower()
            icon_hashed_filename = str(uuid.uuid4().hex) + '.' + extension
            file_path            = os.path.join('app/static/uploads/group_icons', icon_hashed_filename)
            icon.save(file_path)
            group.group_icon = icon_hashed_filename

    group.name = request.form.get('name')
    group.about = request.form.get('about')
   
    db.session.commit()
    return jsonify(group.to_json()) # change this to better message format

@api.route('/interest_groups/<int:id>', methods=['DELETE'])
@login_required
def delete_interest_group(id):
    """
    DELETE an Interest Group by ID
    ---
    tags:
      - groups

    parameters:

        - name: id
          in: path
          description: Group ID
          type: integer
          required: true
          default: 1

    responses:
      200:
        description: OK
      500:
        description: Error
    """
    interest_group = Interest_Group.query.filter_by(id=id).delete()
    
    try:
        db.session.commit()
        return jsonify({'status':'success'}), 200
    except exc.SQLAlchemyError:
        db.session.rollback()
        return jsonify({'status': 'error'}), 404

@api.route('/interest_groups/<int:id>/members')
@login_required
def get_members(id):
    """
    Get all members of a Group
    ---
    tags:
      - groups

    parameters:

        - name: id
          in: path
          description: Group ID
          type: integer
          required: true
          default: 1

    responses:
      200:
        description: OK
        schema:
          id: users
          properties:
            id:
                type: integer
                example: 1

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
                type: integer
                example: 1
                description: Corresponding values for Administrator, Manager, and User
      500:
        description: Error
    """

    group = Interest_Group.query.get_or_404(id)

    members = User.query.join(Membership).join(Interest_Group).filter(Interest_Group.id == group.id)
    return jsonify([
        user.to_json() for user in members
    ])

@api.route('/interest_groups/<int:id>/role')
@login_required
def get_role_by_group(id):
    """
    Get Role of current user to a Group
    ---
    tags:
      - groups

    parameters:
      - name: id
        in: path
        example: 1
        required: true
        type: int
        description: Group id
    responses:
      200:
        description: OK
        schema:
            id: role
            properties:
                role:
                    type: string
                    example: regular
                    required: true
                    default: None
            
    """
    status_code = Membership.query\
        .filter(Membership.group_id == id, Membership.user_id == current_user.get_id())\
        .first()

    if(status_code != None):
        return jsonify({'role': 'regular' if status_code.level == 0 else 'leader'})
    else:
        return jsonify({'role': 'None'})

@api.route('/interest_groups/<int:id>/join', methods=['POST'])
@login_required
def join_group(id):
    """
    Joining Group
    ---
    tags:
        - groups
    parameters:
        - name: id
          in: path
          type: int
          example: 1
          description: Group ID

    responses:
        200:
            description: Success
        409:
            description: Record Exists
        500:
            description: Internal Server Error
    """    
    membership = Membership(
        user_id=current_user.get_id(),
        group_id=id)
    db.session.add(membership)

    try:
        db.session.commit()
        return jsonify({'message': 'Success'}), 201
    except exc.IntegrityError as e:
        db.session().rollback()
        return jsonify({'message': 'Record exists'}), 409

@api.route('/interest_groups/<int:id>/join/status')
@login_required
def get_request_status(id):
    """
    Joinig Status to a Group
    ---
    tags:
        - groups
    parameters:
        - name: id
          in: path
          type: int
          example: 1
          description: Group ID

    responses:
        200:
            description: Success
            schema:
                id: membership
                properties:
                    membership_status:
                        type: string
                        example: pending
                        default: None
                        required: true
                    membership_level:
                        type: string
                        example: regular
                        required: true
                        default: None
        409:
            description: Record Exists
        500:
            description: Internal Server Error
    """    
    status_code = Membership.query\
        .filter(Membership.group_id == id)\
        .filter(Membership.user_id == current_user.get_id())\
        .first()

    if(status_code != None):
        return jsonify({'membership_status': 'pending', 'membership_level': 'regular'} if status_code.status == 0 else {'membership_status': 'accepted', 'membership_level': 'regular' if status_code.level == 0 else 'leader'})
    else:
        return jsonify({'membership_status': 'None'})

@api.route('/interest_groups/<int:id>/leave', methods=['DELETE'])
@login_required
def leave_group(id):
    """
    Leave a group
    ---
    tags:
      - groups

    parameters:
      - name: id
        in: path
        description: Group ID
        type: integer
        required: true
        default: 1

    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    membership = Membership.query.filter(\
        Membership.user_id==current_user.get_id(),
        Membership.group_id==id).delete()

    if membership == 1:
        return jsonify({'status': 'Success'}), 200
    else:
        return jsonify({'status': 'Not Found'}), 404

@api.route('/interest_groups/<int:id>/activities')
@login_required
def group_activities_by(id):
    """
    Activities of a group
    ---
    tags:
      - groups

    parameters:
      - name: id
        in: path
        description: Group ID
        type: integer
        required: true
        default: 1

    responses:
      200:
        description: OK
      404:
        description: Not Found
    """

    activities = Activity.query                          \
                    .join(Interest_Group)                \
                    .filter(Interest_Group.id == id)   \
                    .all()

    return jsonify([
            activity.to_json() for activity in activities
        ])

@api.route('/interest_groups/<int:group_id>/accept', methods=['POST'])
def accept_request(group_id):
    user_id = int(request.form.get('user_id'));
    membership = Membership.query.filter(Membership.group_id == group_id, Membership.user_id == user_id).first()
    membership.status = 1
    db.session.commit()
    return jsonify({'status': 'Success'}), 200

@api.route('/interest_groups/<int:group_id>/decline', methods=['POST'])
def decline_request(group_id):
    user_id = int(request.form.get('user_id'));
    membership = Membership.query.filter(Membership.group_id == group_id, Membership.user_id == user_id).first()
    membership.status = 3
    db.session.commit()
    return jsonify({'status': 'Success'}), 200

