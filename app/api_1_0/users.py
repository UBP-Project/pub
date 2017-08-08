from flask import jsonify, request, current_app, url_for
from app.models import User
from app.api_1_0 import api
from app import db
import json
from flask_login import login_required

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
