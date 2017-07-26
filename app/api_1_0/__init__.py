from flask import Blueprint

api = Blueprint('api', __name__)

from app.api_1_0 import activities, interest_groups, users, errors, authentication

# from app.api_1_0.crud import crud, authentication, error
# from app.models import User
# from app.models import Activity
# from app.models import Interest_Group

# crud(api, User, 'users')
# crud(api, Activity, 'activities')
# crud(api, Interest_Group, 'interest_groups')