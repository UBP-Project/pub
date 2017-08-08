from flask import jsonify, request, url_for
from .. import db
import json
from ..models import Interest_Group, Membership, User
from . import api
from flask_login import login_required, current_user
import datetime
from sqlalchemy import exc

@api.route('/interest_groups')
@login_required
def get_interest_groups():

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
def get_interest_group(id):
    interest_group = Interest_Group.query.get_or_404(id)
    return jsonify(interest_group.to_json()), 200

@api.route('/interest_groups/', methods=['POST'])
@login_required
def new_interest_group():
    data = request.form.to_dict()
    interest_group = Interest_Group.from_json(data)
    try:
        db.session.add(interest_group)
        db.session.commit()
        return jsonify(interest_group.to_json()), 201, \
            {'Location': url_for('api.new_interest_group', id=interest_group.id, _external=True)}
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': 'Name already taken'}), 409

@api.route('/interest_groups/<int:id>', methods=['PUT'])
@login_required
def edit_interest_group(id):
    interest_group = Interest_Group.query.filter_by(id=id).update(request.form.to_dict())
    db.session.commit()
    return jsonify(interest_group.to_json()) # change this to better message format

@api.route('/interest_groups/<int:id>', methods=['DELETE'])
@login_required
def delete_interest_group(id):
    interest_group = Interest_Group.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify(interest_group.to_json()), 200

# @api.route('/interest_groups/<int:id>/join', methods=['GET', 'POST'])
# @login_required
# def join_interest_group(id):
#     user_id = current_user.get_id()
#     membership = Membership(
#         user_id=user_id,
#         id=id,
#         status=1,
#         level='regular')
#     db.session.add(membership)
#     db.session.commit()
#     return jsonify(membership.to_json()), 201, \
#         {'Location': url_for('api.join_interest_group', id=id, _external=True)}

@api.route('/interest_groups/<int:id>/members')
@login_required
def get_members(id):
    members = User.query\
        .join(Membership)\
        .join(Interest_Group)\
        .filter(Interest_Group.id == id)

    return jsonify([
        user.to_json() for user in members
    ])

@api.route('/interest_groups/<int:id>/role')
@login_required
def get_role(id):
    if 'user_id' in request.args:
        user_id = request.args.get('user_id')

        status_code = Membership.query\
            .filter(Membership.group_id == id, Membership.user_id == user_id)\
            .first()

        if(status_code != None):
            return jsonify({'role': 'regular' if status_code.level == 0 else 'leader'})
        else:
            return jsonify({'role': 'None'})
    else:
        return jsonify({'status': 'error'}), 404

@api.route('/interest_groups/<int:id>/join', methods=['POST'])
@login_required
def join_group(id):
    try:
        membership = Membership(
            user_id=current_user.get_id(),
            group_id=id)
        db.session.add(membership)
        db.session.commit()

        return jsonify({'message': 'Success'}), 201
    except exc.IntegrityError as e:
        db.session().rollback()
        return jsonify({'message': 'Record exists'}), 409

@api.route('/interest_groups/<int:id>/join/status')
@login_required
def get_request_status(id):
    if 'user_id' in request.args:
        user_id = request.args.get('user_id')

        status_code = Membership.query\
            .filter(Membership.group_id == id)\
            .filter(Membership.user_id == user_id)\
            .first()

        if(status_code != None):
            return jsonify({'membership_status': 'pending'} if status_code.status == 0 else {'membership_status': 'accepted', 'membership_level': 'regular' if status_code.level == 0 else 'leader'})
        else:
            return jsonify({'membership_status': 'None'})
    else:
        return jsonify({'status': 'error'}), 404

@api.route('/interest_groups/<int:id>/leave', methods=['DELETE'])
@login_required
def leave_group(id):
        membership = Membership.query.filter(\
            Membership.user_id==1,
            Membership.group_id==id).delete()

        if membership == 1:
            return jsonify({'message': 'Success'}), 200
        else:
            return jsonify({'message': 'Not Found'}), 404