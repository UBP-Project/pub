from app.api_1_0 import api
from flask_login import current_user
from app.models import Activity, User, Interest_Group, Perks
from flask import jsonify, request
from datetime import datetime, date, time, timedelta
from sqlalchemy import or_, func

LIMIT_ALL_ACTIVITIES = 3
LIMIT_ALL_GROUPS = 4
LIMIT_ALL_PERKS = 4
LIMIT_ALL_USERS = 3


@api.route('/search', methods=['GET'])
def search():
    # filter by type, groups, users, activities, perks, all
    f = request.args.get('filter', 'all')
    q = request.args.get('query')

    if q is None:
        return None

    if f == 'groups':
        groups = search_groups()
        return jsonify({
            'filter': 'groups',
            'results': { 'groups': [group.to_json() for group in groups.items] },
            'has_next': groups.has_next
        })
    elif f == 'activities':
        activities = search_activities()
        return jsonify({
            'filter': 'activities',
            'results': { 'activities': [activity.to_json() for activity in activities.items] },
            'has_next': activities.has_next
        })
    elif f == 'users':
        users = search_users()
        return jsonify({
            'filter': 'users',
            'results': { 'users': [user.to_json() for user in users.items] },
            'has_next': users.has_next
        })
    elif f == 'perks':
        perks = search_perks()
        return jsonify({
            'filter': 'perks',
            'results': { 'perks': [perk.to_json() for perk in perks.items] },
            'has_next': perks.has_next
        })
    else:
        # get top 3 of each
        groups = Interest_Group.query.filter(or_(
            Interest_Group.name.ilike("%" + q + "%"),
            Interest_Group.about.ilike("%" + q + "%")))\
            .limit(LIMIT_ALL_GROUPS)

        users = User.query.filter(or_(
            User.firstname.ilike("%" + q + "%"),
            User.middlename.ilike("%" + q + "%"),
            User.lastname.ilike("%" + q + "%"),
            User.email.ilike("%" + q + "%"),
            User.department.ilike("%" + q + "%"),
            User.position.ilike("%" + q + "%"),
            func.concat(User.firstname, ' ', User.lastname).contains(q),
            func.concat(User.lastname, ' ', User.firstname).contains(q),
            func.concat(User.firstname, ' ', User.middlename, ' ', User.lastname).contains(q))
        ).limit(LIMIT_ALL_USERS)

        activities = Activity.query.filter(
            or_(Activity.title.ilike("%" + q + "%"),
                Activity.description.ilike("%" + q + "%")))\
            .order_by(Activity.start_date.desc())\
            .limit(LIMIT_ALL_ACTIVITIES)

        perks = Perks.query.filter(or_(
            Perks.title.ilike("%" + q + "%"),
            Perks.description.ilike("%" + q + "%")
        )).order_by(Perks.timestamp.desc()).limit(LIMIT_ALL_PERKS)

        return jsonify({
            "filter": "all",
            "results": {
                "activities": [activity.to_json() for activity in activities],
                "users": [user.to_json() for user in users],
                "groups": [group.to_json() for group in groups],
                "perks": [perk.to_json() for perk in perks]
            },
            'has_next': False # we're only returning partial results since filter == all
        });


def search_groups():
    q = request.args.get('query')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 9))

    groups = Interest_Group.query.filter(or_(
            Interest_Group.name.ilike("%" + q + "%"),
            Interest_Group.about.ilike("%" + q + "%")))\
            .order_by(Interest_Group.name)\
            .paginate(page=page, per_page=per_page, error_out=False)

    return groups


def search_activities():
    q = request.args.get('query')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 8))

    activities = Activity.query.filter(
        or_(Activity.title.ilike("%" + q + "%"),
            Activity.description.ilike("%" + q + "%")))\
        .order_by(Activity.start_date.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return activities


def search_users():
    q = request.args.get('query')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 8))

    users = User.query.filter(or_(
            User.firstname.ilike("%" + q + "%"),
            User.middlename.ilike("%" + q + "%"),
            User.lastname.ilike("%" + q + "%"),
            User.email.ilike("%" + q + "%"),
            User.department.ilike("%" + q + "%"),
            User.position.ilike("%" + q + "%"),
            func.concat(User.firstname, ' ', User.lastname).contains(q),
            func.concat(User.lastname, ' ', User.firstname).contains(q),
            func.concat(User.firstname, ' ', User.middlename, ' ', User.lastname).contains(q))
        ).paginate(page=page, per_page=per_page, error_out=False)

    return users


def search_perks():
    q = request.args.get('query')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 4))

    perks = Perks.query.filter(or_(
            Perks.title.ilike("%" + q + "%"),
            Perks.description.ilike("%" + q + "%")
        )).order_by(Perks.timestamp.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return perks
