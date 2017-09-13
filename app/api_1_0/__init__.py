from flask import Blueprint

api = Blueprint('api', __name__)

from app.api_1_0 import activities, interest_groups, users, notifications, feed, decorators