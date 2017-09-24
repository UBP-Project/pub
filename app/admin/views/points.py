from flask import render_template, redirect, url_for, request
from .. import admin
from app import db
from app.models import Points_Type, Points, User
from ...decorators import admin_required

@admin.route('/points')
@admin_required
def points():
	return render_template('admin/points/points.html')
