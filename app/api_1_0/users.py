from flask import jsonify, request, current_app, url_for
from app.models import User, Follow
from app.api_1_0 import api
from app import db
import json
from flask_login import login_required, current_user

@api.route('/users')
@login_required
def get_users():
    users = User.query.all()
    return jsonify([
        user.to_json() for user in users
    ])

@api.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def user(id):
    if request.method == 'GET':
        users = User.query.get_or_404(id)
        return jsonify(users.to_json())

    elif request.method == 'PUT':
        user = User.query.filter_by(id=id).update(request.form.to_dict())
        db.session.commit()
        return "Updated" # change this to better message format

    else:
        user = User.query.filter_by(id=id).delete()
        db.session.commit()
        return "Deleted"

@api.route('/users', methods=['POST'])
@login_required
def new_user():
    data = request.form.to_dict()
    user = User.from_json(data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_json()), 201, \
        {'Location': url_for('api.new_user', id=user.id, _external=True)}

@api.route('/users/follow/<int:to_follow_id>', methods=['POST'])
@login_required
def follow_user(to_follow_id):
    follow = Follow(follower_id=current_user.get_id(), following_id=to_follow_id)
    db.session.add(follow)
    db.session.commit()
    return jsonify({'message': 'Success'}), 200

@api.route('/users/unfollow/<int:to_unfollow_id>', methods=['POST'])
@login_required
def unfollow_user(to_unfollow_id):
    follow = Follow.query.filter(Follow.follower_id==current_user.get_id(),\
        Follow.following_id==to_unfollow_id).delete()
    db.session.commit()
    return jsonify({'message': 'Success'}), 200