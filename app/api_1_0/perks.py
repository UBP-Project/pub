from app.models import Perks
from app.api_1_0 import api
from flask import jsonify, request
from flask_login import login_required

PERKS_PER_PAGE = 6

@api.route('/perks', methods=['GET'])
@login_required
def get_perks():
    page = 1
    if 'page' in request.args:
        page = int(request.args.get('page'))
    perks = Perks.query.order_by(Perks.timestamp)\
        .paginate(page = page, per_page=PERKS_PER_PAGE, error_out=False)
    return jsonify({
        'perks': [ perk.to_json() for perk in perks.items ],
        'has_next': perks.has_next,
        'has_prev': perks.has_prev
    })