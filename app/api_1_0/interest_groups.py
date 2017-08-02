from flask import jsonify, request, url_for
from .. import db
import json
from ..models import Interest_Group, Membership
from . import api
from flask_login import login_required, current_user
import datetime

@api.route('/interest_groups/')
def get_interest_groups():
    interest_groups = Interest_Group.query.all()
    return jsonify({
        'interest_groups': [interest_group.to_json() for interest_group in interest_groups]
    }), 200

@api.route('/interest_groups/<int:id>')
def get_interest_group(id):
    interest_group = Interest_Group.query.get_or_404(id)
    return jsonify(interest_group.to_json()), 200

@api.route('/interest_groups/', methods=['POST'])
def new_interest_group():
    data = request.form.to_dict()
    interest_group = Interest_Group.from_json(data)
    db.session.add(interest_group)
    db.session.commit()
    return jsonify(interest_group.to_json()), 201, \
        {'Location': url_for('api.new_interest_group', id=interest_group.id, _external=True)}

@api.route('/interest_groups/<int:id>', methods=['PUT'])
def edit_interest_group(id):
    interest_group = Interest_Group.query.filter_by(id=id).update(request.form.to_dict())
    db.session.commit()
    return jsonify(interest_group.to_json()) # change this to better message format

@api.route('/interest_groups/<int:id>', methods=['DELETE'])
def delete_interest_group(id):
    interest_group = Interest_Group.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify(interest_group.to_json()), 200

@api.route('/interest_groups/join/<int:group_id>', methods=['POST'])
@login_required
def join_interest_group(group_id):
    user_id = current_user['id']
    membership = Membership(
        user_id=user_id,
        group_id=group_id,
        status=1,
        level='regular')
    db.session.add(membership)
    db.session.commit()
    return jsonify(membership.to_json()), 201, \
        {'Location': url_for('api.join_interest_group', group_id=group_id, _external=True)}



