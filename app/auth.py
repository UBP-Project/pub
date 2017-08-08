from .models import User, Membership
from flask_login import current_user
from flask import abort


# helper function to check
# if the current user can perform manager or leader permissions
def manager_or_leader_only(group_id):
    canAccess = Membership.query.filter(Membership.user_id == current_user.get_id(),\
        Membership.group_id == group_id) is not None
    if canAccess == None:
        abort(403)

