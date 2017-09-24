from flask import jsonify, request, current_app, url_for
from flask_login import login_required, current_user
from sqlalchemy import exc
from app.models import User, Follow, Notification, Interest_Group, Membership, Points, Activity, User_Activity
from app.api_1_0 import api#, follow_notif
from app import db
import json
from app.notification import Notif
from sqlalchemy import func, or_

@api.route('/users')
@login_required
def get_users():
    """
    Get list of all Users
    ---
    tags:
      - users

    parameters:
      - name: limit
        in: query
        example: 1
        default: 10

    responses:
        200:
            description: OK
            schema:
                id: users
                properties:
                    id:
                        type: string
                        example: 1
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
    if 'limit' in request.args:
        limit = request.args.get('limit')
        users = User.query.order_by(User.firstname).limit(limit)
    elif 'query' in request.args:
        query = request.args.get('query')
        q = query.lower().strip()
        users = User.query\
        .filter(or_(
            User.firstname.ilike("%"+str(q)+"%"),
            User.middlename.ilike("%"+str(q)+"%"), 
            User.lastname.ilike("%"+str(q)+"%"),
            User.email.ilike("%"+str(q)+"%"),
            User.department.ilike("%"+str(q)+"%"),
            User.position.ilike("%"+str(q)+"%"),
            func.concat(User.firstname, ' ', User.lastname).contains(q),
            func.concat(User.lastname, ' ', User.firstname).contains(q),
            func.concat(User.firstname, ' ', User.middlename, ' ', User.lastname).contains(q))
        ).order_by(User.firstname).all()
    else:
        users = User.query.order_by(User.firstname).all()
    return jsonify({"users":[
        user.to_json() for user in users
    ]}), 200

@api.route('/users/<uuid(strict=False):id>')
@login_required
def get_user_by(id):
    """
    Get User by id
    ---
    tags:
      - users

    parameters:
      - name: id
        in: path
        type: string
        example: 0f5b5ff8-afa2-43f7-8066-8ec3075c4c0c

    responses:
      200:
        description: OK
        schema:
            id: users
            properties:
                id:
                    type: string
                    example: 1
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
      404:
        description: Not Found
    """
    users = User.query.get_or_404(id)
    return jsonify(users.to_json())

@api.route('/users/<uuid(strict=False):id>', methods=['PUT'])
@login_required
def edit_user_by(id):
    """
    Edit User by id
    ---
    tags:
      - users

    parameters:
      - name: id
        in: path
        type: string
        example: 0f5b5ff8-afa2-43f7-8066-8ec3075c4c0c
        required: true

      - name: firstname
        in: formData
        type: string
        example: Juan

      - name: middlename
        in: formData
        type: string
        example: Clinton

      - name: lastname
        in: formData
        type: string
        example: dela Cruz

      - name: email
        in: formData
        type: string
        example: jdc@gmail.com

      - name: department
        in: formData
        type: string
        example: Business Analytics

      - name: position
        in: formData
        type: string
        example: Project Hire

      - name: birthday
        in: formData
        type: string
        format: date
        example: 1997-09-07

    responses:
        200:
            description: OK
        500:
            description: Internal Server Error
    """
    user = User.query.filter_by(id=id).update(request.form.to_dict())

    try:
        db.session.commit()
        return "Updated" # change this to better message format
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500

@api.route('/users/<uuid(strict=False):id>', methods=['DELETE'])
@login_required
def delete_user_by(id):
    """
    Delete User by id
    ---
    tags:
      - users

    parameters:
      - name: id
        in: path
        type: string
        example: 0f5b5ff8-afa2-43f7-8066-8ec3075c4c0c

    responses:
        200:
            description: OK
        404:
            description: Not Found
        500:
            description: Internal Server Error
    """
    user = User.query.filter_by(id=id).delete()

    
    try:
        db.session.commit()
        return "Deleted"
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500

@api.route('/users', methods=['POST'])
@login_required
def new_user():
    """
    Create New User
    ---
    tags:
      - users

    parameters:
      - name: firstname
        in: formData
        type: string
        example: Juan
        required: true

      - name: middlename
        in: formData
        type: string
        example: Clinton

      - name: lastname
        in: formData
        type: string
        example: dela Cruz
        required: true

      - name: email
        in: formData
        type: string
        example: jdc@gmail.com
        required: true

      - name: department
        in: formData
        type: string
        example: Business Analytics
        required: true

      - name: position
        in: formData
        type: string
        example: Project Hire
        required: true

      - name: birthday
        in: formData
        type: string
        format: date
        example: 1997-09-07
        required: true

      - name: role_id
        in: formData
        type: string
        format: date
        example: 38409e73-d561-4589-954c-cbfd9f7a7f97
        required: true
        description: The value for USER type role id depends on the database

    responses:
        200:
            description: OK
        500:
            description: Internal Server Error
    """
    data = request.form.to_dict()
    user = User.from_json(data)
    db.session.add(user)

    try:
        db.session.commit()
        return jsonify(user.to_json()), 201, \
            {'Location': url_for('api.new_user', id=user.id, _external=True)}
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500

@api.route('/users/<uuid(strict=False):to_follow_id>/follow', methods=['POST'])
@login_required
def follow_user(to_follow_id):
    """
    Follow User
    ---
    tags:
      - users

    parameters:
      - name: to_follow_id
        in: path
        type: string
        example: 38409e73-d561-4589-954c-cbfd9f7a7f97
        required: true

    responses:
        200:
            description: OK
        500:
            description: Internal Server Error
    """

    follow = Follow(follower_id=current_user.get_id(), following_id=to_follow_id)
    db.session.add(follow)

    try:
        db.session.commit()
       
        #Notification
        notification = Notif('user', 'followed_you', to_follow_id)

        #who triggered this action?
        notification.add_actor(current_user.get_id())

        # for follower in followers:
        #     notif = Notification(user_id=follower.get_id(), content=content, url=url)
        #     db.session.add(notif)

        # db.session.commit()

        return jsonify({'status': 'Success'}), 200
    except exc.IntegrityError as d:
        db.session.rollback()
        print(d)
        return jsonify({'status': 'Record already exists'}), 201
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500
    
@api.route('/users/<uuid(strict=False):to_unfollow_id>/unfollow', methods=['DELETE'])
@login_required
def unfollow_user(to_unfollow_id):
    """
    Unfollow User
    ---
    tags:
      - users

    parameters:
      - name: to_unfollow_id
        in: path
        type: string
        example: 38409e73-d561-4589-954c-cbfd9f7a7f97
        required: true

    responses:
        200:
            description: OK
        500:
            description: Internal Server Error
    """
    follow = Follow.query.filter(Follow.follower_id==current_user.get_id(),\
        Follow.following_id==to_unfollow_id).delete()

    #Notification
    notification = Notif.notif_object(entity='user', action='followed_you', entity_id=to_unfollow_id)

    #who triggered this action?
    if notification:
        notification.set_inactive()

    db.session.commit()
    return jsonify({'message': 'Success'}), 200

@api.route('/users/<string:id>/followers', methods=['GET'])
def get_followers(id):
    followers = current_user.get_followers()
    followings_current_user = current_user.get_followings()
    for follower in followers:
        if follower in followings_current_user:
            follower.isFollowing = True
        else:
            follower.isFollowing = False

    return jsonify({
        'followers': [follow_item_to_json(follower) for follower in followers]
    })

@api.route('/users/<string:id>/followings', methods=['GET'])
def get_followings(id):
    followings = User.query.join(Follow, Follow.following_id == User.id)\
        .order_by(Follow.timestamp.desc())\
        .filter(Follow.follower_id == id).all()
    followings_current_user = User.query.join(Follow, Follow.following_id == User.id)\
        .filter(Follow.follower_id == current_user.get_id()).all()
    for following in followings:
        if following in followings_current_user:
            following.isFollowing = True
        else:
            following.isFollowing = False

    return jsonify({
        'followings': [{
        'id'         : following.id,
        'firstname'  : following.firstname,
        'lastname'   : following.lastname,
        'department' : following.department,
        'position'   : following.position,
        'image'      : following.image,
        'isFollowing': following.isFollowing
    } for following in followings]
    })

@api.route('/leaderboard')
@login_required
def leaderboard():
    """
    Get list of Leading of users in the system
    ---
    tags:
    - users

    responses:
        200:
            description: OK
            schema:
            id: users
            properties:
                id:
                type: string
                example: 1
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
    leaders = db.session.query(Points_Type, func.sum(Points_Type.value).label('points'))\
                .join(Points)\
                .join(User)\
                .add_columns(User.firstname, User.middlename, User.lastname, User.id, User.image)\
                .group_by(Points.user_id)\
                .order_by('points DESC')\
                .all()

    return jsonify([ {
        'id' : leader.id,
        'firstname' : leader.firstname,
        'middlename': leader.middlename,
        'lastname'  : leader.lastname,
        'points'    : int(leader.points)
    } for leader in leaders])

@api.route('/isCorrectPassword', methods=['POST'])
@login_required
def is_correct_password():
    password = request.form.get('password')
    print(password)
    if current_user.verify_password(password):
        return jsonify({'is_correct_password': True}), 200
    else:
        return jsonify({'is_correct_password': False}), 200

@api.route('/myactivities/joined')
@login_required
def my_joined_activities():
    """
    Get joined activities by user
    ---
    tags:
      - users
    parameters:
      - name: page
        in: query
        type: integer
        example: 1
        required: true
    responses:
        200:
            description: OK
            schema:
                id: acitivites
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
    if 'page' in request.args:
        page = int(request.args.get('page'))
    else:
        page = 1

    activities = Activity.query\
                .join(User_Activity)\
                .join(User)\
                .filter(User.id == current_user.get_id(), User_Activity.status == 1)\
                .paginate(page=page, per_page=8, error_out=False)

    return jsonify({
        'has_next': activities.has_next,
        'has_prev': activities.has_prev,
        'joined_activities': [activity.to_json() for activity in activities.items]}), 200

@api.route('/myactivities/interested')
def my_interested_activities():
    """
    Get interested activities by user
    ---
    tags:
      - users
    parameters:
      - name: page
        in: query
        type: integer
        example: 1
        required: true

    responses:
        200:
            description: OK
            schema:
                id: acitivites
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
    if 'page' in request.args:
        page = int(request.args.get('page'))
    else:
        page = 1

    activities = Activity.query\
                .join(User_Activity)\
                .join(User)\
                .filter(User.id == current_user.get_id(), User_Activity.status == 0)\
                .paginate(page=page, per_page=10, error_out=False)

    return jsonify({
        'has_next': activities.has_next,
        'has_prev': activities.has_prev,
        'interested_activities': [activity.to_json() for activity in activities.items]}), 200

@api.route('/mygroups/joined')
@login_required
def my_groups():
    """
    Get joined groups by user
    ---
    tags:
      - users

    parameters:
      - name: page
        in: query
        type: integer
        example: 1
        required: true
    
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

    groups = Interest_Group.query\
                .join(Membership)\
                .join(User)\
                .filter(User.id == current_user.get_id(), Membership.status == Membership.MEMBERSHIP_ACCEPTED)\
                .paginate(page=page, per_page=8, error_out=False)

    return jsonify({
        'has_next': groups.has_next,
        'has_prev': groups.has_prev,
        'mygroups': [group.to_json() for group in groups.items]}), 200

@api.route('/mygroups/pending')
@login_required
def my_pending_groups():
    """
    Get pending request to join groups by user
    ---
    tags:
      - users

    parameters:
      - name: page
        in: query
        type: integer
        example: 1
        required: true
    
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

    groups = Interest_Group.query\
                .join(Membership)\
                .join(User)\
                .filter(User.id == current_user.get_id(), Membership.status == Membership.MEMBERSHIP_PENDING)\
                .paginate(page=page, per_page=8, error_out=False)

    return jsonify({
        'has_next': groups.has_next,
        'has_prev': groups.has_prev,
        'mygroups': [group.to_json() for group in groups.items]}), 200