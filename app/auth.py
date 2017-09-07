from .models import User, Membership, Role
from flask_login import current_user
from flask import abort


# helper function to check
# if the current user can perform manager or leader permissions
def is_manager_or_leader(abort_on_false=False):
    membership = Membership.query.filter(Membership.user_id == current_user.get_id(),
        (Membership.level == 1) | (Membership.level == 2)).first() is not None

    if membership == False and abort_on_false == True:
        abort(403)
        return False
  
    if membership == False:
        return False
    return True

def is_manager(abort_on_false=False):
    isManager = User.query\
            .join(Role, Role.id == User.role_id)\
            .filter(Role.name == 'Manager', User.id == current_user.get_id()).first() is not None
    if abort_on_false == True and isManager == False:
        abort(403)
    return isManager

