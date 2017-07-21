from flask import Blueprint
from app.api.restplus import api

blueprint = Blueprint('api', __name__, url_prefix='/api')
api.init_app(blueprint)