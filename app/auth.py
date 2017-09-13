from .models import User, Membership, Role, Activity, Interest_Group
from flask_login import current_user
from flask import abort


# helper function to check
# if the current user can perform manager or leader permissions
def is_manager_or_leader(abort_on_false=False):
    can_access = Membership.query.filter(Membership.user_id == current_user.get_id(),
        (Membership.level == 1) | (Membership.level == 2)).first() is not None
    if can_access == False and abort_on_false == True:
        abort(403)
    return can_access

def can_modify_activity(activity_id, abort_on_false=False):
    can_access = Membership.query.join(Activity, Activity.group_id == Membership.group_id)\
        .filter(Membership.user_id == current_user.get_id(),
        (Membership.level == 1) | (Membership.level == 2), Activity.id == activity_id).first() is not None
    if can_access == False and abort_on_false == True:
        abort(403)
    return can_access

def can_accept_requests(group_id, abort_on_false=False):
    can_access = Membership.query.join(Interest_Group, Interest_Group.id == Membership.group_id)\
        .filter(Membership.user_id == current_user.get_id(), 
            (Membership.level == 1) | (Membership.level == 2),
            Interest_Group.id == group_id).first() is not None
    if can_access == False and abort_on_false == True:
        abort(403)
    return can_access

def can_modify_group(group_id, abort_on_false=False):
    can_access = Membership.query.join(Interest_Group, Interest_Group.id == Membership.group_id)\
        .filter(Membership.user_id == current_user.get_id(), Membership.level == 2,
            Interest_Group.id == group_id).first() is not None
    if can_access == False and abort_on_false == True:
        abort(403)
    return can_access

def is_manager(abort_on_false=False):
    isManager = User.query\
            .join(Role, Role.id == User.role_id)\
            .filter(Role.name == 'Manager', User.id == current_user.get_id()).first() is not None
    if abort_on_false == True and isManager == False:
        abort(403)
    return isManager

