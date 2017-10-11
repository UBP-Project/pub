from flask import Blueprint

client = Blueprint('client', __name__)

from . import views, errors, users, activities, groups, perks
