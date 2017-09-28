from flask import jsonify
from flask_login import login_required, current_user
from sqlalchemy import exc
from app.models import Points_Type, Points, User
from app import db
from app.api_1_0 import api
from sqlalchemy import func

@api.route('/mypoints')
@login_required
def mypoints():
	"""
    Get the total points and point history of current user
    ---
    tags:
        - points

    responses:
        200:
            description: OK
            schema:
                id: points
                properties:
                    point_history:
                        properties:
                        	id:
                        		type: string
                        	event:
                        		type: string
                        	timestamp:
                        		type: string
                        	value: int
                    total_points:
                      	type: int

        404:
            description: Not Found
    """

	points = db.session.query(Points, func.sum(Points.value).label('points'))\
			.join(User)\
			.group_by(Points.user_id)\
			.filter(User.id == current_user.get_id())\
			.first()\
			.points

	points_history = Points.query\
			.join(User)\
			.add_columns(Points.id, Points.timestamp, Points.event, Points.value)\
			.filter(User.id == current_user.get_id())\
			.order_by(Points.timestamp.desc())\
			.all()
			

	return jsonify({
		'total_points' : int(points),
		'points_history' : [
			{
				'id'		: point.id,
				'timestamp' : point.timestamp,
				'event'		: point.event,
				'value'		: point.value
			} for point in points_history
		]
	}), 200

@api.route('/user/<string:id>/points')
@login_required
def points(id):
	points = db.session.query(Points_Type, func.sum(Points_Type.value).label('points'))\
			.join(Points).join(User)\
			.group_by(Points.user_id)\
			.filter(User.id == id)\
			.first()\
			.points

	return jsonify({
		'total_points' : int(points)
	}), 200