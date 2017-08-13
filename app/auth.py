from .models import User, Membership
from flask_login import current_user
from flask import abort


# helper function to check
# if the current user can perform manager or leader permissions
def manager_or_leader_only(group_id, abort_on_false=True):
    membership = Membership.query.filter(Membership.user_id == current_user.get_id(),\
        Membership.group_id == group_id, Membership.level == 1).first()

    if membership is None and abort_on_false == True:
        abort(403)
        return False
  
    if membership is None:
        return False
    return True

