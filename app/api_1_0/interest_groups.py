from flask import jsonify, request, url_for
from .. import db
import json
from ..models import Interest_Group, Activity
from . import api

@api.route('/interest_groups/')
def get_interest_groups():
    return "Query List of Interest_Group"

@api.route('/interest_groups/', methods=['POST'])
def new_interest_group():
    data = request.form.to_dict()
    interest_group = Interest_Group.from_json(data)
    db.session.add(interest_group)
    db.session.commit()
    return jsonify(interest_group.to_json()), 201, \
        {'Location': url_for('api.new_interest_group', id=interest_group.id, _external=True)}
