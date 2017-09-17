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
      - name: page
        in: query
        example: 1
        default: 1

    responses:
      200:
        description: OK
        schema:
          id: groups
          properties:
            id:
                type: string
                example: 04cb8787-fe54-4e73-80d4-c17bf56537ee

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
    if 'page' in request.args:
        page = int(request.args.get('page'))
    else:
        page = 1

    interest_groups = Interest_Group.query\
        .outerjoin(Membership) \
        .outerjoin(User) \
        .with_entities(
            Interest_Group.id,              \
            Interest_Group.name,            \
            Interest_Group.about,           \
            Interest_Group.cover_photo,     \
            Interest_Group.group_icon,      \
            Membership.status
            )  \
        .paginate(page = page, per_page = 8, error_out=False)

    return jsonify({
      'interest_groups': [ 
            {
                'id': group.id,
                'name': group.name,
                'about': group.about,
                'cover_photo': group.cover_photo,
                'group_icon': group.group_icon,
                'membership_status': group.status
            }
            for group in interest_groups.items ],
      'has_next': interest_groups.has_next,
      'has_prev': interest_groups.has_prev
    }), 200
       
@api.route('/groups', methods=['GET'])
@login_required
def get_groups():
    if 'page' in request.args:
        page = int(request.args.get('page'))
    else:
        page = 1
    groups = Interest_Group.query\
        .paginate(page = page, per_page = 12, error_out=False)
    return jsonify({
      'interest_groups': [ group.to_json() for group in groups.items ],
      'has_next': groups.has_next,
      'has_prev': groups.has_prev
    })

@api.route('/groups/<string:id>/members', methods=['GET'])
@login_required
def get_group_members(id):

    group = Interest_Group.query.get(id)

    leaders = group.get_leaders()
    members = group.get_members()
    managers = group.get_managers()
    return jsonify({
        'members': [ member.to_json() for member in members],
        'leaders': [ leader.to_json() for leader in leaders],
        'managers':[ manager.to_json() for manager in managers]
    });

@api.route('/groups/<string:id>/activities', methods=['GET'])
@login_required
def get_group_activities(id):
    activities = Activity.query.filter(Activity.group_id == id).all()
    return jsonify({
        'activities': [activity.to_json() for activity in activities]
    })


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

@api.route('/interest_groups/<string:id>')
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
        example: 04cb8787-fe54-4e73-80d4-c17bf56537ee
        type: string
        required: true

    responses:
        200:
            description: OK
            schema:
                id: groups
                properties:
                    id:
                        type: string
                        example: 27e2200d-0da1-4dbf-bc9c-7c930ea1d75c
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


@api.route('/interest_groups/<string:id>', methods=['PUT'])
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
          type: string
          required: true
          default: 27e2200d-0da1-4dbf-bc9c-7c930ea1d75c

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

@api.route('/interest_groups/<string:id>', methods=['DELETE'])
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
          type: string
          required: true
          default: 27e2200d-0da1-4dbf-bc9c-7c930ea1d75c

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

@api.route('/interest_groups/<string:id>/members')
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
          type: string
          required: true
          default: 27e2200d-0da1-4dbf-bc9c-7c930ea1d75c

    responses:
        200:
            description: OK
            schema:
                id: users
                properties:
                    id:
                        type: string
                        example: 0f5b5ff8-afa2-43f7-8066-8ec3075c4c0c

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
        500:
            description: Error
    """

    group = Interest_Group.query.get_or_404(id)

    members = User.query\
        .join(Membership, User.id == Membership.user_id)\
        .join(Interest_Group, Interest_Group.id == group.id)\
        .filter(Membership.level == Membership.MEMBERSHIP_MEMBER, Membership.status == Membership.MEMBERSHIP_ACCEPTED)\
        .all()

    return jsonify([
        user.to_json() for user in members
    ])

@api.route('/interest_groups/<string:id>/role')
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
        example: 04cb8787-fe54-4e73-80d4-c17bf56537ee
        required: true
        type: string
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

@api.route('/interest_groups/<string:id>/join', methods=['POST'])
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
          type: string
          example: 0f5b5ff8-afa2-43f7-8066-8ec3075c4c0c
          description: Group ID

    responses:
        200:
            description: Success
        409:
            description: Record Exists
        500:
            description: Internal Server Error
    """    
    membership = Membership(user_id=current_user.get_id(),group_id=id)
    
    db.session.add(membership)

    try:
        db.session.commit()
        return jsonify({'message': 'Success'}), 201
    except exc.IntegrityError as e:
        db.session().rollback()
        return jsonify({'message': 'Record exists'}), 409

@api.route('/interest_groups/<string:id>/join/status')
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
          type: string
          example: 0f5b5ff8-afa2-43f7-8066-8ec3075c4c0c
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

@api.route('/interest_groups/<string:id>/leave', methods=['DELETE'])
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
        type: string
        required: true
        default: 0f5b5ff8-afa2-43f7-8066-8ec3075c4c0c

    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    membership = Membership.query\
        .filter(\
            Membership.user_id==current_user.get_id(),\
            Membership.group_id==id,\
        ).delete()

    if membership:
        db.session.commit()
        return jsonify({'status': 'Success'}), 200
    else:
        return jsonify({'status': 'Not Found'}), 404

@api.route('/interest_groups/<string:id>/activities')
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
        type: string
        required: true
        default: 0f5b5ff8-afa2-43f7-8066-8ec3075c4c0c

    responses:
      200:
        description: OK
      404:
        description: Not Found
    """

    activities = Activity.query                          \
        .filter(Activity.group_id == id)   \
        .all()

    print(activities)
    
    return jsonify([
            activity.to_json() for activity in activities
        ])

@api.route('/interest_groups/<string:id>/leaders', methods=['GET'])
def get_group_leaders(id):
    """
    Get the list of leaders of the group
    ---
    tags:
      - groups

    parameters:
      - name: id
        in: path
        description: Group ID
        type: string
        required: true
        default: 0f5b5ff8-afa2-43f7-8066-8ec3075c4c0c

    responses:
      200:
        description: OK
      404:
        description: Not Found
    """

    group = Interest_Group.query.get_or_404(id)

    leaders = User.query.join(Membership, User.id == Membership.user_id).join(Interest_Group, Interest_Group.id == group.id)\
        .filter(Membership.level == Membership.MEMBERSHIP_LEADER).all()
    
    return jsonify([
        leader.to_json() for leader in leaders
    ])

@api.route('/interest_groups/<string:group_id>/accept', methods=['POST'])
def accept_request(group_id):
    user_id = request.form.get('user_id');
    membership = Membership.query.filter(Membership.group_id == group_id, Membership.user_id == user_id).first()
    membership.status = 1
    db.session.commit()
    return jsonify({'status': 'Success'}), 200

@api.route('/interest_groups/<string:group_id>/decline', methods=['POST', 'GET'])
def decline_request(group_id):
    user_id = request.form.get('user_id');
    membership = Membership.query.filter(Membership.group_id == group_id, Membership.user_id == user_id).first()
    membership.status = 3
    db.session.commit()
    return jsonify({'status': 'Success'}), 200

@api.route('/interest_groups/<string:group_id>/requests', methods=['GET'])
def get_requests(group_id):
    requests = Membership.query.join(User, User.id == Membership.user_id)\
        .add_columns(User.firstname, User.lastname,
            User.department, User.position, User.image,
            User.id.label("user_id"), Membership.group_id)\
        .filter(Membership.group_id == group_id, Membership.status == 0).all()
    return jsonify({
        'requests': [{
            'group_id'  : request.group_id,
            'user_id'   : request.user_id,
            'firstname' : request.firstname,
            'lastname'  : request.lastname,
            'image'     : request.image,
            'department': request.department,
            'position'  : request.position
        } for request in requests]
    }), 200

@api.route('/interest_groups/<string:group_id>/setleader', methods=['POST'])
def set_leader(group_id):
    user_id = request.form.get('user_id');
    membership = Membership.query.filter(Membership.group_id == group_id, Membership.user_id == user_id).first()
    membership.level = 1
    db.session.commit()
    return jsonify({'status': 'Success'}), 200

@api.route('/interest_groups/<string:group_id>/remove_leader', methods=['POST'])
def remove_leader(group_id):
    user_id = request.form.get('user_id');
    membership = Membership.query.filter(Membership.group_id == group_id, Membership.user_id == user_id).first()
    membership.level = 0
    db.session.commit()
    return jsonify({'status': 'Success'}), 200

@api.route('/interest_groups/<string:group_id>/remove', methods=['POST'])
def remove_member(group_id):
    user_id = request.form.get('user_id');
    membership = Membership.query.filter(Membership.group_id == group_id, Membership.user_id == user_id).first()
    db.session.delete(membership)
    db.session.commit()
    return jsonify({'status': 'Success'}), 200

@api.route('/interest_groups/mygroups')
def my_groups():
    groups = Interest_Group.query\
                .join(Membership)\
                .join(User)\
                .filter(User.id == current_user.get_id())\
                .all()

    return jsonify([group.to_json() for group in groups]), 200