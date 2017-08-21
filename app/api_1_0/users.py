from flask import jsonify, request, current_app, url_for
from flask_login import login_required, current_user
from sqlalchemy import exc
from app.models import User, Follow, Notification
from app.api_1_0 import api
from app.api_1_0.decorators import follow_notif
from app import db
import json

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
        users = User.query.limit(limit)
    else:
        users = User.query.all()
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

    print(current_user)
    #follows you notification
    

    try:
        db.session.commit()
        return jsonify({'status': 'Success'}), 200
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
    db.session.commit()
    return jsonify({'message': 'Success'}), 200

@api.route('/leaderboard')
def leaderboard():
    leaders = User.query.order_by(User.points.desc()).limit(10)
    return jsonify([leader.to_json() for leader in leaders])
