from flask import jsonify
from sqlalchemy import exc
from app.models import Points_Type, Points, User
from app import db
from app.api_1_0 import api