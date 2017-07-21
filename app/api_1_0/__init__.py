from flask import Blueprint

api = Blueprint('api', __name__)

from . import activities, interest_groups